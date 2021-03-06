#!/usr/bin/env python3

"""
Make histograms of the jet pt spectra
"""

from argparse import ArgumentParser
from h5py import File
from glob import glob
import numpy as np
import json, os

from common import get_denom_dict, get_dsid
from common import is_dijet, is_ditop, is_dihiggs, is_wz
from cross_section import CrossSections

def get_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('datasets', nargs='+')
    parser.add_argument('-d', '--denominator', required=True)
    parser.add_argument('-x', '--cross-sections', required=True)
    parser.add_argument('-o', '--out-dir', default='pt-hists')
    return parser.parse_args()

def get_hist(ds, edges):
    hist = None
    print(glob('%s/*.h5'%ds))
    print(ds)
    for fpath in glob('%s/*.h5'%ds):
        print(fpath)
        with File(fpath,'r') as h5file:
            pt = h5file.get('fat_jet')['pt']
            weight = h5file.get('fat_jet')['mcEventWeight']
            assert pt is not None
            assert weight is not None
            if hist is None:
                hist = np.histogram(pt, edges, weights=weight)[0]
            else:
                hist += np.histogram(pt, edges, weights=weight)[0]
    assert hist is not None
    return hist

def get_hist_reweighted(ds, edges, ratio):
    hist = None
    for fpath in glob('%s/*.h5'%ds):
        with File(fpath,'r') as h5file:
            pt = h5file['fat_jet']['pt']
            indices = np.digitize(pt, edges) - 1
            weight = ratio[indices]
            assert len(pt[pt<0]) == 0, pt[pt<0] # no negative pt
            if hist is None:
                hist = np.histogram(pt, edges, weights=weight)[0]
            else:
                hist += np.histogram(pt, edges, weights=weight)[0]
    assert hist is not None
    return hist


def draw_hist(hist, edges, out_dir, parts={}, file_name='dijet.pdf'):
    from mpl import Canvas
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    centers = 1e-6 * (edges[1:] + edges[:-1]) / 2
    gev_per_bin = (centers[2] - centers[1]) * 1e3
    with Canvas('%s/%s'%(out_dir, file_name)) as can:
        can.ax.plot(centers, hist)
        can.ax.set_yscale('log')
        can.ax.set_ylabel('jets * fb / %f TeV'%gev_per_bin)
        can.ax.set_xlabel(r'Fat Jet $p_{\rm T}$ [TeV]')
        maxval = can.ax.get_ylim()[1]
        can.ax.set_ylim(0.1, maxval)
        for dsid, part in parts.items():
            can.ax.plot(centers, part, label=str(dsid))
        can.ax.legend(ncol=2)

def save_hist(hist, edges, out_dir, file_name, group_name):
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    with File('%s/%s'%(out_dir, file_name),'a') as h5file:
        hist_group = h5file.create_group(group_name)
        hist_group.create_dataset('hist', data=hist)
        hist_group.create_dataset('edges', data=edges)

def run():
    args = get_args()
    edges = np.concatenate([[-np.inf], np.linspace(0, 3e6, 101), [np.inf]])
    out_hists = os.path.join(args.out_dir, 'jetpt.h5')
    if os.path.isfile(out_hists):
        os.remove(out_hists)
    run_dijet(edges, args)
    run_higgs(edges, args)
    run_higgs_reweighted(edges, args)
    run_ditop(edges, args)
    run_ditop_reweighted(edges, args)
    run_wz(edges, args)
    run_wz_reweighted(edges, args)

def run_dijet(edges, args):
    with open(args.denominator, 'r') as denom_file:
        denom = get_denom_dict(denom_file)
    with open(args.cross_sections, 'r') as xsec_file:
        xsecs = CrossSections(xsec_file, denom)

    parts = {}
    hist = 0
    for ds in args.datasets:
        dsid = get_dsid(ds)
        print("Current dataset is dijet", dsid)
        if not is_dijet(dsid):
            continue
        if xsecs.datasets[dsid]['denominator'] == 0:
            continue
        weight = xsecs.get_weight(dsid)
        # get_hist() gives the histogram weighted by mcEventWeight
        this_dsid = get_hist(ds, edges) * weight
        parts[dsid] = np.array(this_dsid)
        hist += this_dsid

    draw_hist(hist, edges, args.out_dir, parts, file_name='dijet.pdf')
    save_hist(hist, edges, args.out_dir, 'jetpt.h5', 'dijet')

def run_higgs(edges, args):
    hist = 0
    parts = {}
    for ds in args.datasets:
        dsid = get_dsid(ds)
        if not is_dihiggs(dsid):
            continue
        print("Current dataset is higgs in run_higgs", dsid)
        this_dsid = get_hist(ds, edges)
        parts[dsid] = np.array(this_dsid)
        hist += this_dsid

    draw_hist(hist, edges, args.out_dir, parts, file_name='higgs.pdf')
    save_hist(hist, edges, args.out_dir, 'jetpt.h5', 'higgs')

def run_higgs_reweighted(edges, args):
    hist = 0
    parts = {}
    out_dir = args.out_dir
    with File('%s/jetpt.h5'%out_dir, 'r') as h5file:
        num = h5file['dijet']['hist']
        denom = h5file['higgs']['hist']
        ratio = np.zeros_like(num)
        valid = np.asarray(denom) > 0.0
        ratio[valid] = num[valid] / denom[valid]  # this is the histograms ratio
        np.save("images/dihiggs_ratio.npy", ratio)
    for ds in args.datasets:
        dsid = get_dsid(ds)
        if not is_dihiggs(dsid):
            continue
        print("Current dataset is Higgs", dsid)
        this_dsid = get_hist_reweighted(ds, edges, ratio)
        parts[dsid] = np.array(this_dsid)
        hist += this_dsid
    print("about to draw higgs_reweight.pdf")
    draw_hist(hist, edges, args.out_dir, parts, file_name='higgs_reweight.pdf')

def run_ditop(edges, args):
    hist = 0 
    parts = {}
    for ds in args.datasets:
        dsid = get_dsid(ds)
        if not is_ditop(dsid):
            continue
        print("Current dataset is top in run_ditop", dsid)
        this_dsid = get_hist(ds, edges)
        parts[dsid] = np.array(this_dsid)
        hist += this_dsid

    draw_hist(hist, edges, args.out_dir, parts, file_name='ditop.pdf')
    save_hist(hist, edges, args.out_dir, 'jetpt.h5', 'ditop')

def run_ditop_reweighted(edges, args):
    hist = 0 
    parts = {}
    out_dir = args.out_dir
    with File('%s/jetpt.h5'%out_dir, 'r') as h5file:
        num = h5file['dijet']['hist']
        denom = h5file['ditop']['hist']
        ratio = np.zeros_like(num)
        valid = np.asarray(denom) > 0.0 
        ratio[valid] = num[valid] / denom[valid]  
        np.save("images/ditop_ratio.npy", ratio)
    for ds in args.datasets:
        dsid = get_dsid(ds)
        if not is_ditop(dsid):
            continue
        print("Current dataset is diTop", dsid)
        this_dsid = get_hist_reweighted(ds, edges, ratio)
        parts[dsid] = np.array(this_dsid)
        hist += this_dsid

    draw_hist(hist, edges, args.out_dir, parts, file_name='ditop_reweight.pdf')

def run_wz(edges, args):
    hist = 0
    parts = {}
    for ds in args.datasets:
        dsid = get_dsid(ds)
        if not is_wz(dsid):
            continue
        print("Current dataset is wz in run_wz", dsid)
        this_dsid = get_hist(ds, edges)
        if this_dsid is not None:
            parts[dsid] = np.array(this_dsid)
            hist += this_dsid
    print(hist)
    draw_hist(hist, edges, args.out_dir, parts, file_name='wz.pdf')
    save_hist(hist, edges, args.out_dir, 'jetpt.h5', 'wz')

def run_wz_reweighted(edges, args):
    hist = 0 
    parts = {}
    out_dir = args.out_dir
    with File('%s/jetpt.h5'%out_dir, 'r') as h5file:
        num = h5file['dijet']['hist']
        denom = h5file['wz']['hist']
        ratio = np.zeros_like(num)
        valid = np.asarray(denom) > 0.0 
        ratio[valid] = num[valid] / denom[valid]  
        np.save("images/wz_ratio.npy", ratio)
    for ds in args.datasets:
        dsid = get_dsid(ds)
        if not is_wz(dsid):
            continue
        print("Current dataset is wz (reweighted)", dsid)
        this_dsid = get_hist_reweighted(ds, edges, ratio)
        parts[dsid] = np.array(this_dsid)
        hist += this_dsid

    draw_hist(hist, edges, args.out_dir, parts, file_name='wz_reweight.pdf')


if __name__ == '__main__':
    run()
