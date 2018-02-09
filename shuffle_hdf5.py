from __future__ import print_function

import numpy as np
import h5py
import sys


path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_5/"

if sys.argv[1] == 'signal':
    signal = True
elif sys.argv[1] == 'bg':
    signal = False
else:
    assert 1==0, "please specify signal or bg"

if signal:
    load_file_name = 'temporary_flattened_data_signal.h5'
    save_file_name = "temporary_flattened_shuffled_data_signal.h5" 
else:
    load_file_name = 'temporary_flattened_data_bg.h5'
    save_file_name = "temporary_flattened_shuffled_data_bg.h5"


load_f = h5py.File(path+load_file_name, 'r')
save_f = h5py.File(path+save_file_name, 'a')

dataset_names = list(load_f.keys())

for dataset_name in dataset_names:
    print(dataset_name)
    data = load_f.get(dataset_name)
    save_data = save_f.get(dataset_name)
    N = data.shape[0]
    new_sizes = {u'clusters': (N, 5, 60),
                 u'jets': (N, 11),
                 u'subjet1': (N, 40),
                 u'subjet2': (N, 40),
                 u'subjet3': (N, 40),
                 u'tracks': (N, 29, 60),
                }   
    if save_data is None:
        save_data = save_f.create_dataset("%s"%(dataset_name), new_sizes[dataset_name], dtype='f')
    assert data.shape[0] == save_data.shape[0]
    num_samples = data.shape[0]
    print("generating random indices")
    indices = range(num_samples)
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

        if num_dims == 1:
            save_data[start:end] = mini_batch
        elif num_dims == 2:
            save_data[start:end, :] = mini_batch
        elif num_dims == 3:
            save_data[start:end, :, :] = mini_batch
    

