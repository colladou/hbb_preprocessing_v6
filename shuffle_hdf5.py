from __future__ import print_function

import numpy as np
import h5py
import sys
import utils

def remove_bad_missing_values(data):
    category_names = utils.get_category_names()
    sub_jet_names = category_names['subjet1']
    if True:
        if data[sub_jet_names.index('JetFitter_nVTX')] == 0:
            print('jet failure')
            data[sub_jet_names.index('JetFitter_energyFraction')] = np.nan
            data[sub_jet_names.index('JetFitter_mass')] = np.nan
            data[sub_jet_names.index('JetFitter_significance3d')] = np.nan
            data[sub_jet_names.index('JetFitter_deltaphi')] = np.nan
            data[sub_jet_names.index('JetFitter_deltaeta')] = np.nan
            data[sub_jet_names.index('JetFitter_massUncorr')] = np.nan
            data[sub_jet_names.index('JetFitter_dRFlightDir')] = np.nan
            data[sub_jet_names.index('JetFitter_nSingleTracks')] = np.nan  
            data[sub_jet_names.index('JetFitter_nTracksAtVtx')] = np.nan
            data[sub_jet_names.index('JetFitter_N2Tpair')] = np.nan
        if data[sub_jet_names.index('SV1_masssvx')] == -1:
            print("mass failure")
            data[sub_jet_names.index('SV1_efracsvx')] = np.nan
            data[sub_jet_names.index('SV1_significance3d')] = np.nan
            data[sub_jet_names.index('SV1_dstToMatLay')] = np.nan
            data[sub_jet_names.index('SV1_deltaR')] = np.nan
            data[sub_jet_names.index('SV1_Lxy')] = np.nan
            data[sub_jet_names.index('SV1_L3d')] = np.nan
            data[sub_jet_names.index('SV1_N2Tpair')] = np.nan
            data[sub_jet_names.index('SV1_NGTinSvx')]= np.nan
    return data


path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/"

assert sys.argv[1] is not None, "Please specify a tag (signal, bg, top, other)"

tag = sys.argv[1]

load_file_name = 'temporary_flattened_data_%s.h5'%tag
save_file_name = "temporary_flattened_shuffled_data_%s.h5"%tag 

load_f = h5py.File(path+load_file_name, 'r')
save_f = h5py.File(path+save_file_name, 'a')

dataset_names = list(load_f.keys())

for dataset_name in dataset_names:
    print(dataset_name)
    data = load_f.get(dataset_name)
    save_data = save_f.get(dataset_name)
    N = data.shape[0]
    new_sizes = {u'fat_jet': (N, 17+1),
                     u'subjet1': (N, 42),
                     u'subjet2': (N, 42),
                     u'subjet3': (N, 42),
                     u'subjet1_tracks': (N, 21, 10), # 10 tracks each with 21 variables
                     u'subjet2_tracks': (N, 21, 10),
                     u'subjet3_tracks': (N, 21, 10),
                     u'weight': (N,)
                    }  
    if save_data is None:
        save_data = save_f.create_dataset("%s"%(dataset_name), new_sizes[dataset_name], dtype='f')
    assert data.shape[0] == save_data.shape[0]
    num_samples = data.shape[0]
    print("generating random indices")
    indices = list(range(num_samples))
    np.random.seed(2)
    np.random.shuffle(indices)
    np.save(path+"randomization_indexes_%s.npy"%sys.argv[1], indices)
    
    batch_size = 1 
    print("copying samples")
    for start, end in zip(range(0, num_samples, batch_size), 
                          range(batch_size, num_samples+batch_size, batch_size)):
        if len(data.shape) == 1:
            mini_batch = data[indices[start:end]]
        elif len(data.shape) == 2:
            mini_batch = data[indices[start:end], :]
        elif len(data.shape) == 3:
            mini_batch = data[indices[start:end], :, :]
        else:
            assert 1==0, 'not implemented'
    
        num_dims = len(mini_batch.shape)
        if dataset_name in [u'subjet1', u'subjet2', u'subjet3']:
            mini_batch = remove_bad_missing_values(mini_batch)

        if num_dims == 1:
            save_data[start:end] = mini_batch
        elif num_dims == 2:
            save_data[start:end, :] = mini_batch
        elif num_dims == 3:
            save_data[start:end, :, :] = mini_batch
    

