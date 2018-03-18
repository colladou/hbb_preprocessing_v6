from __future__ import print_function

import numpy as np
import h5py
import utils
import sys
from glob import glob

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
        
    #np.save("%s_original_to_new" % file_name.replace('.h5', ''), original_to_new)
    #np.save(path+"new_to_original_%s" % sys.argv[1], new_to_original)

category_names = utils.get_category_names()

# Merges many hdf5 files into one
data_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/"

tag = sys.argv[1]
assert tag is not None, "please specify a tag (signal, bg, other)"

new_file_dataset_name = "temporary_flattened_data_%s.h5"%tag

if tag == "signal":
    round_down = 1.0 # This is in case you want to use only a percentage of the samples in each file, default is to use all (1.0) 
elif tag=='bg':
    round_down = 10.0 
else:
    round_down = 1.0

#feature_names = [u'fat_jet']
feature_names = [u'fat_jet', u'subjet1', u'subjet2', u'subjet3', u'subjet1_tracks', u'subjet2_tracks', u'subjet3_tracks', 'weight']

# This list can contain the names of many h5 files and it will merge them into one.

file_list = []

if tag == 'signal':
    f_names = glob(data_path+'dihiggs/*/*.h5')
elif tag=='bg':
    f_names = glob(data_path+'dijet/*/*.h5')
else:
    f_names = ['output.h5']
          
for f_name in f_names:
    file_list.append(f_name)
   
files = []
for f_name in f_names:
    files.append(h5py.File(f_name, 'r'))

# Calculate total samples
total_samples = utils.count_num_samples_from_hdf5_file_list(f_names, round_down, feature_names=feature_names)
print("total samples", total_samples)

new_to_original = {}

new_hdf5 = h5py.File(data_path + new_file_dataset_name, 'w')
#for feature_name in ['weight']:
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
        
    
        if feature_name != 'weight':
            col_names = category_names[feature_name]
        assert data is not None
        N = int(total_samples)
        new_sizes = {u'fat_jet': (N, 17+1),
                     u'subjet1': (N, 42),
                     u'subjet2': (N, 42),
                     u'subjet3': (N, 42),
                     u'subjet1_tracks': (N, 21, 10), # 10 tracks each with 21 variables
                     u'subjet2_tracks': (N, 21, 10),
                     u'subjet3_tracks': (N, 21, 10),
                     u'weight': (N,)
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
        if feature_name != 'weight':
            data = data[col_names]  # enforce a label order # It seems this doesnt work...
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
            if feature_name == 'weight':
                data = data[0:num_samples_this_file]
            else:
                data = utils.flatten(data[0:num_samples_this_file])

            raw_data = f.get(feature_name)
            #assert np.nanmean(data[:, 0]) == np.nanmean(raw_data[col_names[0]]), [np.nanmean(data[:, 0]), np.nanmean(raw_data[col_names[0]])]            
            #print(col_names[0], np.nanmean(data[:, 0]), np.nanmean(raw_data[col_names[0]]))
            save_data[start:end] = data
        elif len(data.shape) == 2:
            data = utils.flatten(data[0:num_samples_this_file, :])
            save_data[start:end, :] = data
        elif len(data.shape) == 3:
            data = utils.flatten(data[0:num_samples_this_file, :, :])
            save_data[start:end, :, :] = data
        start = start + num_samples_this_file
