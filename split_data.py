import h5py
import numpy as np
import sys

def save_splitted_random_indexes(load_path, set_divisions):
    full_indexes = np.load(load_path+'randomization_indexes_%s.npy' % sys.argv[1])
    for set_name, value in set_divisions.items():
        set_start, set_end = value[1], value[2]
        indexes = full_indexes[set_start:set_end]
        np.save(load_path+"random_indexes_%s_%s" % (set_name, sys.argv[1]), indexes)

def round_number(x, batch_size=100):
    return int(np.floor(x/batch_size)*batch_size)

def calculate_set_divisions(total_samples, split_vector, batch_size):
    start = 0
    set_divisions = {}
    for name in ['valid', 'test', 'train']:  # change the order of the sets here for cross validation
        num_samples = round_number(split_vector[name]*total_samples, batch_size)
        set_start = start
        set_end = start + num_samples
        set_divisions[name] = (num_samples, set_start, set_end)
        start = set_end
    return set_divisions

load_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_5/"

if sys.argv[1] == 'signal':
    load_and_save_file_names = [["temporary_flattened_shuffled_data_signal.h5", "temporary_flattened_shuffled_divided_data_signal.h5"]]
elif sys.argv[1] == 'bg':
    load_and_save_file_names = [["temporary_flattened_shuffled_data_bg.h5", "temporary_flattened_shuffled_divided_data_bg.h5"]]
else:
    assert 1==0, "please specify signal or bg"
for load_file_name, save_file_name in load_and_save_file_names:
    #split_vector = (0.7, 0.15, 0.15)
    split_vector = {'train': 0.7, 'valid': 0.15, 'test': 0.15}
    batch_size=100

    load_f = h5py.File(load_path + load_file_name, 'r')
    save_f = h5py.File(load_path + save_file_name, 'a')

    for feature in load_f.keys():
        print feature
        data = load_f.get(feature)
        #size = data.shape
        set_divisions = calculate_set_divisions(data.shape[0], split_vector, batch_size)
        #save_splitted_random_indexes(load_path, set_divisions)
        
        for set_name, value in set_divisions.items():
            size = list(data.shape)
            size[0] = value[0]
            set_start, set_end = value[1], value[2]
            print(set_name, set_start, set_end, value)
            dset = save_f.create_dataset("%s/%s"%(feature, set_name), size, dtype='f')
        
            for start, end in zip(range(set_start, set_end, batch_size), range(set_start+batch_size, set_end+batch_size, batch_size)):
                # start and end don't match the ones from the loading set, they should start at zero!
                if len(size) == 1:
                    dset[start-set_start:end-set_start] = data[start:end]
                elif len(size) == 2:
                    dset[start-set_start:end-set_start, :] = data[start:end, :]
                elif len(size) == 3:
                    dset[start-set_start:end-set_start, :, :] = data[start:end, :, :]
                else:
                    assert 1==0, "not implemented"

            # copy the data to the new subdivision
