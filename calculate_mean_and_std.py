import numpy as np
import h5py
import utils
from utils import flatten

def subsample(data, num_samples, shuffled=True):
    num_dims = len(data.shape)
    indices = range(num_samples)
    if not shuffled:
        indices = range(data.shape[0])
        np.random.shuffle(indices)
        indices = indices[0:num_samples]
        indices = list(np.sort(indices))
    if num_dims == 1:
        data = data[indices]
    elif num_dims == 2:
        data = data[indices, :]
    elif num_dims == 3:
        data = data[indices, :, :]
    else:
        assert 1==0, "not implemented" 
    print(data.shape)
    return data

if __name__ == "__main__":
    #assert 1==0, "this calculates statistics of different files, we need to merge them, also change subsampling value"
    print("this is using the same amount of signal and bg, make sure this is what you want")
    save_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/divided_statistics/"
    load_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/"
    file_name_signal = "categorized_data_divided_signal.h5"
    file_name_bg = "categorized_data_divided_bg.h5"
    file_name_top = "categorized_data_divided_top.h5"   
 
    signal_hf = h5py.File(load_path + file_name_signal, 'r')
    bg_hf = h5py.File(load_path + file_name_bg, 'r')
    top_hf = h5py.File(load_path + file_name_top, 'r')
    feature_names = signal_hf.keys()
    #for feature_name in ['mv2c10+']:
    for feature_name in feature_names:
        print("Processing feature %s" % feature_name)
        signal_data = signal_hf.get(feature_name + '/train')
        bg_data = bg_hf.get(feature_name + '/train')
        top_data = top_hf.get(feature_name + '/train')
        assert signal_data is not None
        assert bg_data is not None
        assert top_data is not None
        print("subsampling...")
        signal_data = subsample(signal_data, 200000)
        bg_data = subsample(bg_data, 200000)
        top_data = subsamples(top_data, 200000)
        if len(signal_data.shape) == 3:
            print("flattening...")
            #data = flatten(data)
            signal_data = utils.reshape_to_flat(signal_data)
            bg_data = utils.reshape_to_flat(bg_data)
            top_data = utils.reshape_to_flat(top_data)
            print(signal_data.shape, bg_data.shape)
        data = np.vstack((signal_data, top_data))
        data = np.vstack((data, bg_data))
        print(data.shape)
        assert data.shape[0] == signal_data.shape[0] + bg_data.shape[0] + top_data.shape[0], data.shape[0]
        print("calculating statistics...")
        mean_vector = np.nanmean(data, axis=0)
        std_vector = np.nanstd(data, axis=0)
        print("saving...")
        np.save(save_path + "%s_mean_vector.npy"%feature_name, mean_vector)
        np.save(save_path + "%s_std_vector.npy"%feature_name, std_vector)



"""
for feature_name in feature_names:
    print "Processing feature %s" % feature_name
    data = hf.get(feature_name)[0:10]
    names = data.dtype.names
    mean_vector = np.zeros(len(names))
    std_vector = np.zeros(len(names))

    for pos, var_name in enumerate(names):
        print "   %s" % var_name
        mean_vector[pos] = np.nanmean(data[var_name])
        std_vector[pos] = np.nanstd(data[var_name])
        np.save(save_path + "%s_mean_vector.npy"%feature_name, mean_vector)
        np.save(save_path + "%s_std_vector.npy"%feature_name, std_vector)
"""       





