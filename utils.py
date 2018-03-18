from __future__ import print_function

import numpy as np
import h5py

def flatten(ds):
    """
    Flattens a named numpy array so it can be used with pure numpy.
    Input: named array
    Output: numpy array

    Example;
    print(flatten(sample_jets[['pt', 'eta']]))
    """
    ftype = [(n, float) for n in ds.dtype.names]
    flat = ds.astype(ftype).view(float).reshape(ds.shape + (-1,))
    swapped = flat.swapaxes(1, len(ds.shape)) # swapping is done to arrange array due to new dimension
    return swapped

def shuffle_samples(data, axis=0):
    """ 
    Shuffles the samples (entries) in a numpy array along the given axis
    Input: numpy array
    Output: shuffled numpy array

    Example
    shuffled_data = shuffle_samples(data)

    Possible improvements:
    in place shuffling
    generalize for more than 3 dimensions
    generalize for any axis (maybe we can do both of this by using string execution)
    """

    assert axis==0, "not yet implemented for other axis"
    num_samples = data.shape[axis]
    num_dimensions = len(data.shape)
    indices = range(num_samples)
    np.random.shuffle(indices)

    if num_dimensions == 1:
        return data[indices]
    elif num_dimensions == 2:
        return data[indices, :]
    elif num_dimensions == 3:
        return data[indices, :, :]
    else:
        assert 1==0, "not implemented but easy to implement"


def count_num_samples_from_hdf5(file_name, round_down=1.0, feature_names=None):
    hf = h5py.File(file_name, 'r')
    if feature_names is None:
        feature_names = hf.keys()
    num_samples = None
    for feature_name in feature_names:
        print(feature_name)
        data = hf.get(feature_name)
        assert data is not None, "%s, %s"%(file_name, feature_name)
        if num_samples is None:
            num_samples = data.shape[0]
            num_samples = np.floor(num_samples/round_down)
        else:
            assert len(data.shape) > 0, (file_name, data.shape)
            assert num_samples == np.floor(data.shape[0]/round_down), "num samples changed for %s  %s"%(file_name, feature_name)
    return num_samples


def count_num_samples_from_hdf5_file_list(list_of_files, round_down=1.0, feature_names=None):
    total_num_samples = 0
    for file_name in list_of_files:
        num_samples = count_num_samples_from_hdf5(file_name, round_down, feature_names)
        total_num_samples += num_samples
    return total_num_samples


def get_size_of_features(file_name):
    pass

def reshape_to_flat(data):
    assert len(data.shape) == 3
    return data.reshape((data.shape[0], data.shape[1] * data.shape[2]))


def get_category_names():
    # True names to use from each category. This is in order to prevent using Truth variables and enforce an order in the variables
    category_names = {}
    category_names['fat_jet'] = ('GhostHBosonsCount', 'pt',  'eta',  'mass',
                              'Angularity', 'Aplanarity', 'C2', 'D2', 'FoxWolfram20',
                              'KtDR', 'Qw', 'PlanarFlow', 'Split12', 'Split23',
                              'Tau21_wta', 'Tau32_wta',
                              'ZCut12', 'e3')
    category_names['subjet1'] = ('DL1_pb', 'DL1_pc', 'DL1_pu',
                                 'IP2D_pb', 'IP2D_pc', 'IP2D_pu', 'IP3D_pb', 'IP3D_pc', 'IP3D_pu',
                                 'JetFitter_N2Tpair', 'JetFitter_dRFlightDir', 'JetFitter_deltaeta',
                                 'JetFitter_deltaphi', 'JetFitter_energyFraction', 'JetFitter_mass', 'JetFitter_massUncorr',
                                 'JetFitter_nSingleTracks', 'JetFitter_nTracksAtVtx', 'JetFitter_nVTX', 'JetFitter_significance3d',
                                 'MV2c10_discriminant',
                                 'SV1_L3d', 'SV1_Lxy',
                                 'SV1_N2Tpair', 'SV1_NGTinSvx',
                                 'SV1_deltaR', 'SV1_dstToMatLay',
                                 'SV1_efracsvx', 'SV1_masssvx',
                                 'SV1_pb', 'SV1_pc', 'SV1_pu', 'SV1_significance3d',
                                 'deta', 'dphi', 'dr',
                                 'eta', 'pt',
                                 'rnnip_pb', 'rnnip_pc', 'rnnip_ptau', 'rnnip_pu'
                                )
    category_names['subjet2'] = category_names['subjet1']
    category_names['subjet3'] = category_names['subjet1']
    category_names['subjet1_tracks'] = ('btag_ip_d0', 'btag_ip_d0_sigma', 'btag_ip_z0', 'btag_ip_z0_sigma',
                                'chiSquared', 'deta', 'dphi', 'dr', 'eta',
                                'numberDoF', 'numberOfInnermostPixelLayerHits',
                                'numberOfNextToInnermostPixelLayerHits', 'numberOfPixelHits',
                                'numberOfPixelHoles', 'numberOfPixelSharedHits', 'numberOfPixelSplitHits',
                                'numberOfSCTHits', 'numberOfSCTHoles', 'numberOfSCTSharedHits',
                                'pt', 'ptfrac')
    category_names['subjet2_tracks'] = category_names['subjet1_tracks']
    category_names['subjet3_tracks'] = category_names['subjet1_tracks']
    return category_names





def test_shuffle_samples():
    # 1 dimension
    np.random.seed(2)
    a = np.asarray(range(4))
    b = shuffle_samples(a)
    c = a[[2, 3, 1, 0]]
    assert np.all(np.equal(b, c))

    np.random.seed(2)
    # 2 dimensions
    a = np.asarray(range(12)).reshape((4,3))
    b = shuffle_samples(a)
    c = a[[2, 3, 1, 0], :]
    assert np.all(np.equal(b, c))

    # 3 dimensions
    np.random.seed(2)
    a = np.asarray(range(24)).reshape((4,3,2))
    b = shuffle_samples(a)
    c = a[[2, 3, 1, 0], :, :]
    assert np.all(np.equal(b, c))

if __name__ == "__main__":
    test_shuffle_samples()

