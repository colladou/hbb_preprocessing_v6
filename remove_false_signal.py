import h5py
import numpy as np
import sys

load_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/"

assert sys.argv[1] is not None, 'please specify signal or bg'

tag = sys.argv[1]

load_file_name = "temporary_flattened_shuffled_data_%s.h5"%tag
save_file_name = "temporary_flattened_shuffled_cleaned_data_%s.h5"%tag

load_f = h5py.File(load_path + load_file_name, 'r')
save_f = h5py.File(load_path + save_file_name, 'a')

fat_jet = load_f.get('fat_jet')
GhostHBosonsCount = fat_jet[:, 0]

if tag == 'signal':
    t = GhostHBosonsCount > 0
    assert len(t) == fat_jet.shape[0]
    indices = [i for i, x in enumerate(t) if x]
    assert len(indices) == np.sum(t), [len(indices), np.sum(t)]
    print("Number of invalid signal samples: ", fat_jet.shape[0]-len(indices), "from", fat_jet.shape[0])
else:
    indices = list(range(fat_jet.shape[0]))

batch_size=1

if True:
    for feature in load_f.keys():
        print(feature)
        data = load_f.get(feature)
        if len(data.shape) == 1:
            size = [len(indices)]
        elif len(data.shape) == 2:
            if False #feature != "fat_jet":
                size = [len(indices), data.shape[1]-1]
            else:
                size = [len(indices), data.shape[1]]
        elif len(data.shape) == 3:
            size = [len(indices), data.shape[1], data.shape[2]]
        else:
            assert 1==0, "no implemented"
       
        dset = save_f.create_dataset("%s"%feature, size, dtype='f')

        for new_i, old_i in enumerate(indices):
            if len(size) == 1:
                dset[new_i] = data[old_i]
            elif len(size) == 2:
                if False #feature != "fat_jet":
                    dset[new_i, :] = data[old_i, 1:]
                else:
                    dset[new_i, :] = data[old_i, :]   
            elif len(size) == 3:
                dset[new_i, :, :] = data[old_i, :, :] 
            else:
                assert 1==0, "not implemented"
