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

if sys.argv[1] == 'signal':
    signal = True
elif sys.argv[1] == 'bg':
    signal = False
else:
    assert 1==0, "please specify signal or bg"

if signal:
    new_file_dataset_name = "temporary_flattened_data_signal.h5"
    round_down = 1.0 # This is in case you want to use only a percentage of the samples in each file, default is to use all (1.0) 
else:
    new_file_dataset_name = "temporary_flattened_data_bg.h5"
    round_down = 10.0 

feature_names = [u'clusters', u'jets', u'subjet1', u'subjet2', u'tracks']

# This list can contain the names of many h5 files and it will merge them into one.
file_list_s = ['d301488_j1.h5', 'd301489_j2.h5',
                   'd301490_j3.h5', 'd301491_j4.h5',
                   'd301492_j5.h5', 'd301493_j6.h5',
                   'd301494_j7.h5', 'd301495_j8.h5',
                   'd301496_j9.h5', 'd301497_j10.h5',
                   'd301498_j11.h5', 'd301499_j12.h5',
                   'd301500_j13.h5', 'd301501_j14.h5',
                   'd301502_j15.h5', 'd301503_j16.h5',
                   'd301504_j17.h5', 'd301505_j18.h5',
                   'd301506_j19.h5', 'd301507_j20.h5',]
file_list_bg = [#'d361020_j26.h5', 'd361021_j27.h5',
                    'd361022_j28.h5', 'd361023_j29.h5',
                    'd361024_j30.h5', 'd361025_j31.h5',
                    'd361026_j32.h5', 'd361027_j33.h5',
                    'd361028_j34.h5', 'd361029_j35.h5',
                    'd361030_j36.h5', 'd361031_j37.h5',
                    'd361032_j38.h5',]  
              
             
if signal:
    file_list = file_list_s
else:
    file_list = file_list_bg

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
        new_sizes = {u'clusters': (N, 5, 60),
                 u'jets': (N, 11),
                 u'subjet1': (N, 40),
                 u'subjet2': (N, 40),
                 u'subjet3': (N, 40),
                 u'tracks': (N, 29, 60),
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
