from __future__ import print_function

import numpy as np
import h5py
import utils
import sys

def create_dataset(open_file, feature_name, shape):
    try:
        return open_file.create_dataset(feature_name, shape, dtype=np.float32)
    except(RuntimeError):
        return open_file.get(feature_name)


def save_index_conversion(file_name, original_indexes, merged_file_indexes, new_to_original):
    original_to_new = {}
    for original, new in zip(original_indexes, merged_file_indexes):
        original_to_new[original] = new
        new_to_original[new] = (original, file_name)
        
    np.save("%s_original_to_new" % file_name.replace('.h5', ''), original_to_new)
    np.save(path+"new_to_original_%s" % sys.argv[1], new_to_original)

category_names = {}
category_names['fat_jet'] = ('Split12', 'Split23', 'Qw', 'PlanarFlow', 'Angularity', 'Aplanarity', 'ZCut12', 'KtDR', 
                             'pt', 'eta', 'mass', 
                             'C2', 'D2', 'e3', 
                             'Tau21_wta', 'Tau32_wta', 'FoxWolfram20')
#category_names['clusters'] = ('pt', 'deta', 'dphi', 'energy', 'mask')
category_names['subjet1'] = ('MV2c10_discriminant', 
                             'DL1_pb', 'DL1_pc', 'DL1_pu', 
                             'IP2D_pb', 'IP2D_pc', 'IP2D_pu', 
                             'IP3D_pb', 'IP3D_pc', 'IP3D_pu', 
                             'SV1_pu', 'SV1_pb', 'SV1_pc', 
                             'rnnip_pu', 'rnnip_pc', 'rnnip_pb', 'rnnip_ptau', 
                             'JetFitter_energyFraction', 'JetFitter_mass', 'JetFitter_significance3d', 
                             'JetFitter_deltaphi', 'JetFitter_deltaeta', 'JetFitter_massUncorr', 'JetFitter_dRFlightDir', 
                             'SV1_masssvx', 'SV1_efracsvx', 'SV1_significance3d', 'SV1_dstToMatLay', 'SV1_deltaR', 'SV1_Lxy', 'SV1_L3d', 
                             'JetFitter_nVTX', 'JetFitter_nSingleTracks', 'JetFitter_nTracksAtVtx', 'JetFitter_N2Tpair', 
                             'SV1_N2Tpair', 'SV1_NGTinSvx', 
                             'GhostBHadronsFinalCount', 'GhostCHadronsFinalCount', 
                             'HadronConeExclTruthLabelID', 'HadronConeExclExtendedTruthLabelID', 
                             'pt', 'eta', 'deta', 'dphi', 'dr')
category_names['subjet2'] = category_names['subjet1']
category_names['subjet1_tracks'] = ('chiSquared', 'numberDoF', 
                                    'btag_ip_d0', 'btag_ip_z0', 'btag_ip_d0_sigma', 'btag_ip_z0_sigma', 
                                    'numberOfInnermostPixelLayerHits', 'numberOfNextToInnermostPixelLayerHits', 'numberOfPixelHits', 
                                    'numberOfPixelHoles', 'numberOfPixelSharedHits', 'numberOfPixelSplitHits', 'numberOfSCTHits', 
                                    'numberOfSCTHoles', 'numberOfSCTSharedHits', 
                                    'pt', 'eta', 'deta', 'dphi', 'dr', 'ptfrac')
category_names['subjet2_tracks'] = category_names['subjet1_tracks']


# Merges many hdf5 files into one
path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/"

tag = sys.argv[1]
assert tag is not None, "please specify a tag (signal, bg, other)"

new_file_dataset_name = "temporary_flattened_data_%s.h5"%tag

if tag == "signal":
    round_down = 1.0 # This is in case you want to use only a percentage of the samples in each file, default is to use all (1.0) 
else:
    round_down = 10.0 

feature_names = [u'fat_jet', u'subjet1', u'subjet2', u'subjet1_tracks', u'subjet2_tracks']

# This list can contain the names of many h5 files and it will merge them into one.
file_list_s = []
file_list_bg = []
             
if tag == 'signal':
    file_list = file_list_s
elif tag == 'bg':
    file_list = file_list_bg
elif tag == 'other':
    file_list = ['output.h5']

f_names = []
for name in file_list:
    f_names.append(path + name)

files = []
for f_name in f_names:
    files.append(h5py.File(f_name, 'r'))

# Calculate total samples
total_samples = utils.count_num_samples_from_hdf5_file_list(f_names, round_down)
print("total samples", total_samples)

new_to_original = {}

new_hdf5 = h5py.File(path + new_file_dataset_name, 'w')
for feature_name in feature_names:
    print(feature_name)
    start = 0
    end = 0
    data = None
    #old_names = None
    for f_name in f_names:
        print("loading %s" % f_name)
        f = h5py.File(f_name)
        data = f.get(feature_name)
        col_names = category_names[feature_name]
        assert data is not None
        N = int(total_samples)
        new_sizes = {u'fat_jet': (N, 17),
                     u'subjet1': (N, 46),
                     u'subjet2': (N, 46),
                     u'subjet1_tracks': (N, 21, 10), # 10 tracks each with 21 variables
                     u'subjet2_tracks': (N, 21, 10),
                    }

        # Create the new empty dataset
        if start == 0:
            create_dataset(new_hdf5, feature_name, new_sizes[feature_name])
         
        end = end + int(np.floor(data.shape[0]/round_down))

        save_data = new_hdf5.get(feature_name)
        # this could be made smaller to acomodate RAM requirements
        num_samples_this_file = int(np.floor(data.shape[0]/round_down))
        print(start, end, data.shape[0], end-start)
        #if old_names is None:
        #    old_names = col_names
        #assert old_names == col_names, old_names + col_names
        data = data[col_names][:] 
        if len(data.shape) == 1:
            data = data[:]
        elif len(data.shape) == 2:
            data = data[:, :]
        elif len(data.shape) == 3:
            data = data[:, :, :]   

        original_indexes = list(range(num_samples_this_file))
        merged_file_indexes = list(range(start, end))
        if feature_name == feature_names[0]:
            save_index_conversion(f_name, original_indexes, merged_file_indexes, new_to_original)

        assert data is not None
        if len(data.shape) == 1:
            data = utils.flatten(data[0:num_samples_this_file])
            save_data[start:end] = data
        elif len(data.shape) == 2:
            data = utils.flatten(data[0:num_samples_this_file, :])
            save_data[start:end, :] = data
        elif len(data.shape) == 3:
            data = utils.flatten(data[0:num_samples_this_file, :, :])
            save_data[start:end, :, :] = data
        start = start + num_samples_this_file
