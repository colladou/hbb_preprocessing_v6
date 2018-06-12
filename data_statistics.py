import h5py
import numpy as np
from glob import glob
import utils

def count_num_window_samples(data_path, feature_name):
    datasets_paths = glob("%s/user.dguest.*.hbbTraining.p1_output.h5"%(data_path))
    total_samples = 0
    total_value_sum = 0
    for ds in datasets_paths:
        for fpath in glob('%s/*.h5'%ds):
            with h5py.File(fpath,'r') as h5file:
                fat_jet = h5file.get('fat_jet')
                total_samples += fat_jet.shape[0]
                total_value_sum += np.nansum(fat_jet[feature_name])
    return total_value_sum / total_samples

if __name__ == "__main__":
    data_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/dijet"
    higgs_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/dihiggs"
    #bg_window_samples, bg_samples = count_num_window_samples(data_path)
    #signal_window_samples, signal_samples = count_num_window_samples(higgs_path)
    """
    for feature_name in ('', 'pt',  'eta',  'mass',
                              'Angularity', 'Aplanarity', 'C2', 'D2', 'FoxWolfram20',
                              'KtDR', 'Qw', 'PlanarFlow', 'Split12', 'Split23',
                              'Tau21_wta', 'Tau32_wta',
                              'ZCut12', 'e3'):
    """
    category_names = utils.get_category_names()
    for feature_name in category_names['fat_jet']:
        print(feature_name, count_num_window_samples(higgs_path, feature_name))

