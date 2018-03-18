import h5py
import numpy as np
from glob import glob


def count_num_window_samples(data_path):
    datasets_paths = glob("%s/user.dguest.*.hbbTraining.p1_output.h5"%(data_path))
    total_window_samples=0
    total_samples = 0
    total_mass = 0
    for ds in datasets_paths:
        for fpath in glob('%s/*.h5'%ds):
            with h5py.File(fpath,'r') as h5file:
                #print(fpath)
                feature_name = 'mass'
                mass = h5file.get('fat_jet')[feature_name]
                num_values_in_window = np.sum((146000 >= mass) & (mass >= 76000))
                print("num window samples", num_values_in_window)
                total_window_samples += num_values_in_window
                total_samples += mass.shape[0]
                total_mass += np.sum(mass)
    print("Average %s"%feature_name, total_mass / total_samples)
    return [total_window_samples, total_samples]

if __name__ == "__main__":
    data_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/dijet"
    higgs_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/dihiggs"
    bg_window_samples, bg_samples = count_num_window_samples(data_path)
    signal_window_samples, signal_samples = count_num_window_samples(higgs_path)
    print("total window signal samples ", signal_window_samples)
    print("total signal samples ", signal_samples)
    print("total window bg samples ", bg_window_samples)
    print("total bg samples ", bg_samples)

