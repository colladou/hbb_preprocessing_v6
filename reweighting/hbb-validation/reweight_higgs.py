from argparse import ArgumentParser
from h5py import File
import numpy as np
import json, os
from glob import glob

from common import get_dsid
from common import is_dijet, is_ditop, is_dihiggs

def get_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('datasets', nargs='+')
    parser.add_argument('-o', '--out-dir', default='pt-hists')
    return parser.parse_args()


def create_reweights_from_ratio(ds, edges, ratio):
    """
    Create the re-weights for a dataset ds based on the provided ratio for each bin(edges)
    then it saves the weights to the hdf5 file of the dataset
    ds: Path to folder containing the dataset
    """
    for fpath in glob('%s/*.h5'%ds):
        with File(fpath,'a') as h5file:
            pt = h5file['fat_jet']['pt']
            mc_event_weight = h5file['fat_jet']['mcEventWeight']
            indices = np.digitize(pt, edges) - 1 # divide the pt values into bins (edges)
            ratio_weight = ratio[indices]  # correct reweight based on each on of the edges (bins)
            # weight = mc_event_weight * ratio_weight[indices] this is not needed since the initial 
            # ratio comparison was done with mvEventWeighted plots
            if h5file.get('weight') is not None:
                del h5file['weight']
            h5file.create_dataset('weight', data=ratio_weight, dtype=np.float32)


def create_higgs_reweights(edges, args):
    """
    Calculates correct weighting ratio for pt from histogram files. Then applies this to each dataset
    """
    out_dir = args.out_dir
    with File('%s/jetpt.h5'%out_dir, 'r') as h5file:
        num = h5file['dijet']['hist']
        denom = h5file['higgs']['hist']
        ratio = np.zeros_like(num)
        valid = np.asarray(denom) > 0.0 
        ratio[valid] = num[valid] / denom[valid]  # This is the ratio I need
    for ds in args.datasets:
        dsid = get_dsid(ds)
        if not is_dihiggs(dsid):
            continue
        create_reweights_from_ratio(ds, edges, ratio)

def create_ditop_reweights(edges, args):
    """ 
    Calculates correct weighting ratio for pt from histogram files. Then applies this to each dataset
    """
    out_dir = args.out_dir
    with File('%s/jetpt.h5'%out_dir, 'r') as h5file:
        num = h5file['dijet']['hist']
        denom = h5file['ditop']['hist']
        ratio = np.zeros_like(num)
        valid = np.asarray(denom) > 0.0 
        ratio[valid] = num[valid] / denom[valid]  # This is the ratio I need
    for ds in args.datasets:
        dsid = get_dsid(ds)
        if not is_ditop(dsid):
            continue
        create_reweights_from_ratio(ds, edges, ratio)

def create_wz_reweights(edges, args):
    """ 
    Calculates correct weighting ratio for pt from histogram files. Then applies this to each dataset
    """
    out_dir = args.out_dir
    with File('%s/jetpt.h5'%out_dir, 'r') as h5file:
        num = h5file['dijet']['hist']
        denom = h5file['wz']['hist']
        ratio = np.zeros_like(num)
        valid = np.asarray(denom) > 0.0 
        ratio[valid] = num[valid] / denom[valid]  # This is the ratio I need
    for ds in args.datasets:
        dsid = get_dsid(ds)
        if not is_ditop(dsid):
            continue
        create_reweights_from_ratio(ds, edges, ratio)

if __name__ == "__main__":
    args = get_args()
    edges = np.concatenate([[-np.inf], np.linspace(0, 3e6, 101), [np.inf]])
    create_higgs_reweights(edges, args)
    create_ditop_reweights(edges, args)
