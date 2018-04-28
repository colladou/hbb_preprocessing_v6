from __future__ import print_function
import sys
import h5py 
import numpy as np
import utils

# TODO update to include mv2c10 in subjets

# Sub selection only happens in the second dimension
def create_dataset(open_file, feature_name, shape):
    try:
        return open_file.create_dataset(feature_name, shape, dtype=np.float32)
    except(RuntimeError):
        return open_file.get(feature_name)


def get_position_indexes_from_names(feature_names):
    original_names = utils.get_category_names()
    sub_selection_indexes = {}
    for feature_group_name in feature_names.keys():
        feature_group = feature_names[feature_group_name]
        if feature_group.__class__ is not tuple:
            feature_group = [feature_group]
        original_group = list(original_names[feature_group_name])
        feature_indexes = []
        for feature_name in feature_group:
            index = original_group.index(feature_name)
            feature_indexes.append(index)
        sub_selection_indexes[feature_group_name] = feature_indexes
    return sub_selection_indexes


def create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order):
    data = []
    for category_name in category_order:
        print(category_name)
        data.append(open_file.get('%s/%s' % (category_name, set_type)))
    for element in data: assert element is not None
    num_samples = data[0].shape[0]
    num_features = 0 
    for key in feature_names:
        multiplicity = 1
        if key == 'subjet1_tracks' or key == 'subjet2_tracks' or key == 'subjet3_tracks':
            multiplicity = 10
        if feature_names[key].__class__ is tuple:
            num_features += len(feature_names[key])*multiplicity
        else:
            num_features += 1 * multiplicity
    print('num_features', num_features)
    save_data = create_dataset(save_file, feature_name, (num_samples, num_features))

    position_indexes = get_position_indexes_from_names(feature_names)    
    sub_selection = []
    for category_name in category_order:
        sub_selection.append(list(position_indexes[category_name]))
 
    total_sub_selection_length = 0 
    for pos, element in enumerate(sub_selection):
        if len(data[pos].shape) > 2:
            total_sub_selection_length += len(element)*data[pos].shape[2]
        else:
            total_sub_selection_length += len(element)
    assert total_sub_selection_length == save_data.shape[1], [total_sub_selection_length, save_data.shape[1]]
    print('sub_selection', sub_selection)
    copy_in_batches(data, save_data, sub_selection)       


def merge_2_datasets(data, save_file, feature_name):
    num_samples = data[0].shape[0]
    num_features_list = []
    sub_selections = []
    for dataset in data:
        num_features_list.append(dataset.shape[1])
        sub_selections.append(list(range(0, dataset.shape[1])))
    total_num_features = int(np.sum(num_features_list))
    save_data = create_dataset(save_file, feature_name, (num_samples, total_num_features))
    sub_selection_length = 0 
    for x in sub_selections:
        sub_selection_length +=len(x)
    assert sub_selection_length == save_data.shape[1]
    copy_in_batches(data, save_data, sub_selections)

 
def create_weights(open_file, save_file, set_type):
    category_order = ['weight']
    feature_name = 'weights/%s' % set_type

    data = open_file.get('%s/%s' % ('weight', set_type))
    assert data is not None
    num_samples = data.shape[0]
    num_features = 1
    save_data = create_dataset(save_file, feature_name, (num_samples,))
    save_data[:] = data[:]

def create_fat_jet(open_file, save_file, set_type):
    category_order = ['fat_jet']
    feature_names = {}
    feature_names['fat_jet'] = ('pt',  'eta',  'mass',
                              'Angularity', 'Aplanarity', 'C2', 'D2', 'FoxWolfram20',
                              'KtDR', 'Qw', 'PlanarFlow', 'Split12', 'Split23',
                              'Tau21_wta', 'Tau32_wta',
                              'ZCut12', 'e3')
    feature_name = 'fat_jet/%s' % set_type
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_kinematic(open_file, save_file, set_type):
    category_order = ['fat_jet']
    feature_names = {}
    feature_names['fat_jet'] = ('pt',  'eta',  'mass',)
    feature_name = 'kinematic/%s' % set_type
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_high_level_clusters(open_file, save_file, set_type):
    category_order = ['fat_jet']
    feature_names = {}
    feature_names['fat_jet'] = ('pt',  'eta', 'mass',
                                'Angularity', 'Aplanarity', 'C2', 'D2', 'FoxWolfram20',
                                'KtDR', 'Qw', 'PlanarFlow', 'Split12', 'Split23',
                                'Tau21_wta', 'Tau32_wta', 
                                'ZCut12', 'e3')
    feature_name = 'hl_clusters/%s' % set_type
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)


def create_subjet1(open_file, save_file, set_type):
    category_order = ['subjet1']
    feature_names = {}
    feature_names['subjet1'] = ('IP2D_pb', 'IP2D_pc', 'IP2D_pu', 'IP3D_pb', 'IP3D_pc', 'IP3D_pu',
                                 'JetFitter_N2Tpair', 'JetFitter_dRFlightDir', 'JetFitter_deltaeta',
                                 'JetFitter_deltaphi', 'JetFitter_energyFraction', 'JetFitter_mass', 'JetFitter_massUncorr',
                                 'JetFitter_nSingleTracks', 'JetFitter_nTracksAtVtx', 'JetFitter_nVTX', 'JetFitter_significance3d',
                                 'SV1_L3d', 'SV1_Lxy',
                                 'SV1_N2Tpair', 'SV1_NGTinSvx',
                                 'SV1_deltaR', 'SV1_dstToMatLay',
                                 'SV1_efracsvx', 'SV1_masssvx',
                                 'SV1_pb', 'SV1_pc', 'SV1_pu', 'SV1_significance3d',
                                 'deta', 'dphi', 'dr',
                                 'eta', 'pt',
                                 'rnnip_pb', 'rnnip_pc', 'rnnip_ptau', 'rnnip_pu'
                               )
    feature_name = 'subjet1/%s' % set_type
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_subjet2(open_file, save_file, set_type):
    category_order = ['subjet2']
    feature_names = {}
    feature_names['subjet2'] = ('IP2D_pb', 'IP2D_pc', 'IP2D_pu', 'IP3D_pb', 'IP3D_pc', 'IP3D_pu',
                                 'JetFitter_N2Tpair', 'JetFitter_dRFlightDir', 'JetFitter_deltaeta',
                                 'JetFitter_deltaphi', 'JetFitter_energyFraction', 'JetFitter_mass', 'JetFitter_massUncorr',
                                 'JetFitter_nSingleTracks', 'JetFitter_nTracksAtVtx', 'JetFitter_nVTX', 'JetFitter_significance3d',
                                 'SV1_L3d', 'SV1_Lxy',
                                 'SV1_N2Tpair', 'SV1_NGTinSvx',
                                 'SV1_deltaR', 'SV1_dstToMatLay',
                                 'SV1_efracsvx', 'SV1_masssvx',
                                 'SV1_pb', 'SV1_pc', 'SV1_pu', 'SV1_significance3d',
                                 'deta', 'dphi', 'dr',
                                 'eta', 'pt',
                                 'rnnip_pb', 'rnnip_pc', 'rnnip_ptau', 'rnnip_pu'
                               )
    feature_name = 'subjet2/%s' % set_type
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_subjet3(open_file, save_file, set_type):
    category_order = ['subjet3']
    feature_names = {}
    feature_names['subjet3'] = ('IP2D_pb', 'IP2D_pc', 'IP2D_pu', 'IP3D_pb', 'IP3D_pc', 'IP3D_pu',
                                 'JetFitter_N2Tpair', 'JetFitter_dRFlightDir', 'JetFitter_deltaeta',
                                 'JetFitter_deltaphi', 'JetFitter_energyFraction', 'JetFitter_mass', 'JetFitter_massUncorr',
                                 'JetFitter_nSingleTracks', 'JetFitter_nTracksAtVtx', 'JetFitter_nVTX', 'JetFitter_significance3d',
                                 'SV1_L3d', 'SV1_Lxy',
                                 'SV1_N2Tpair', 'SV1_NGTinSvx',
                                 'SV1_deltaR', 'SV1_dstToMatLay',
                                 'SV1_efracsvx', 'SV1_masssvx',
                                 'SV1_pb', 'SV1_pc', 'SV1_pu', 'SV1_significance3d',
                                 'deta', 'dphi', 'dr',
                                 'eta', 'pt',
                                 'rnnip_pb', 'rnnip_pc', 'rnnip_ptau', 'rnnip_pu'
                               )   
    feature_name = 'subjet3/%s' % set_type
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_high_level_tracks(open_file, save_file, set_type):
    category_order = ['fat_jet', 'subjet1', 'subjet2']
    feature_name = 'hl_tracks/%s' % set_type
    feature_names = {}
    feature_names['fat_jet'] = ('pt',  'eta', 'mass')
    feature_names['subjet1'] = ('IP2D_pb', 'IP2D_pc', 'IP2D_pu', 'IP3D_pb', 'IP3D_pc', 'IP3D_pu',
                                 'JetFitter_N2Tpair', 'JetFitter_dRFlightDir', 'JetFitter_deltaeta',
                                 'JetFitter_deltaphi', 'JetFitter_energyFraction', 'JetFitter_mass', 'JetFitter_massUncorr',
                                 'JetFitter_nSingleTracks', 'JetFitter_nTracksAtVtx', 'JetFitter_nVTX', 'JetFitter_significance3d',
                                 'SV1_L3d', 'SV1_Lxy',
                                 'SV1_N2Tpair', 'SV1_NGTinSvx',
                                 'SV1_deltaR', 'SV1_dstToMatLay',
                                 'SV1_efracsvx', 'SV1_masssvx',
                                 'SV1_pb', 'SV1_pc', 'SV1_pu', 'SV1_significance3d',
                                 'deta', 'dphi', 'dr',
                                 'eta', 'pt',
                                 'rnnip_pb', 'rnnip_pc', 'rnnip_ptau', 'rnnip_pu'
                               )
    feature_names['subjet2'] = feature_names['subjet1']   
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_single_jet_predictions(open_file, save_file, set_type, label_type):
    assert 1==0, "update this method"
    feature_name = 'single_jet_predictions/%s' % set_type
    data_path = '/home/baldig-projects/julian/atlas/hbb/v_6/single_jet_hl_tracks/50_50/'
    data = np.load(data_path + 'predictions_%s_%s.npy' % (set_type, label_type))
    assert data is not None, "could not load data"
    num_samples, num_features = data.shape[0], data.shape[1]
    save_data = create_dataset(save_file, feature_name, (num_samples, num_features))
    sub_selection = [0, 1]
    copy_in_batches(data, save_data, sub_selection)

def create_mv2c10(open_file, save_file, set_type):
    category_order = ['subjet1', 'subjet2']
    feature_name = 'mv2c10/%s' % set_type
    feature_names = {}
    feature_names['subjet1'] = ('MV2c10_discriminant')
    feature_names['subjet2'] = feature_names['subjet1']
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_DL1(open_file, save_file, set_type):
    category_order = ['subjet1', 'subjet2']
    feature_name = 'dl1/%s' % set_type
    feature_names = {}
    feature_names['subjet1'] = ('DL1_pb', 'DL1_pc', 'DL1_pu')
    feature_names['subjet2'] = feature_names['subjet1']
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_mv2c10_plus(open_file, save_file, set_type):
    category_order = ['subjet1', 'subjet2']
    feature_name = 'mv2c10+/%s' % set_type
    feature_names = {}
    #feature_names['fat_jet'] = ('pt',  'eta', 'mass')
    feature_names['subjet1'] = ('MV2c10_discriminant', 'deta', 'dphi', 'dr',)
    feature_names['subjet2'] = feature_names['subjet1']
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)


def create_tracks(open_file, save_file, set_type):
    category_order = ['fat_jet', 'subjet1_tracks', 'subjet2_tracks']
    feature_name = 'tracks/%s' % set_type
    feature_names = {}
    feature_names['fat_jet'] = ('pt',  'eta', 'mass')
    feature_names['subjet1_tracks'] = ('btag_ip_d0', 'btag_ip_d0_sigma', 'btag_ip_z0', 'btag_ip_z0_sigma',
                                       'chiSquared', 'deta', 'dphi', 'dr', 'eta',
                                       'numberDoF', 'numberOfInnermostPixelLayerHits',
                                       'numberOfNextToInnermostPixelLayerHits', 'numberOfPixelHits',
                                       'numberOfPixelHoles', 'numberOfPixelSharedHits', 'numberOfPixelSplitHits',
                                       'numberOfSCTHits', 'numberOfSCTHoles', 'numberOfSCTSharedHits',
                                       'pt', 'ptfrac'
                                      )
    feature_names['subjet2_tracks'] = feature_names['subjet1_tracks']
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_subjet1_tracks(open_file, save_file, set_type):
    category_order = ['subjet1_tracks']
    feature_name = 'subjet1_tracks/%s' % set_type
    feature_names = {}
    #feature_names['fat_jet'] = ('pt',  'eta', 'mass')
    feature_names['subjet1_tracks'] = ('btag_ip_d0', 'btag_ip_d0_sigma', 'btag_ip_z0', 'btag_ip_z0_sigma',
                                       'chiSquared', 'deta', 'dphi', 'dr', 'eta',
                                       'numberDoF', 'numberOfInnermostPixelLayerHits',
                                       'numberOfNextToInnermostPixelLayerHits', 'numberOfPixelHits',
                                       'numberOfPixelHoles', 'numberOfPixelSharedHits', 'numberOfPixelSplitHits',
                                       'numberOfSCTHits', 'numberOfSCTHoles', 'numberOfSCTSharedHits',
                                       'pt', 'ptfrac'
                                      )
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_subjet2_tracks(open_file, save_file, set_type):
    category_order = ['subjet2_tracks']
    feature_name = 'subjet2_tracks/%s' % set_type
    feature_names = {}
    #feature_names['fat_jet'] = ('pt',  'eta', 'mass')
    feature_names['subjet2_tracks'] = ('btag_ip_d0', 'btag_ip_d0_sigma', 'btag_ip_z0', 'btag_ip_z0_sigma',
                                       'chiSquared', 'deta', 'dphi', 'dr', 'eta',
                                       'numberDoF', 'numberOfInnermostPixelLayerHits',
                                       'numberOfNextToInnermostPixelLayerHits', 'numberOfPixelHits',
                                       'numberOfPixelHoles', 'numberOfPixelSharedHits', 'numberOfPixelSplitHits',
                                       'numberOfSCTHits', 'numberOfSCTHoles', 'numberOfSCTSharedHits',
                                       'pt', 'ptfrac'
                                      )
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_subjet3_tracks(open_file, save_file, set_type):
    category_order = ['subjet3_tracks']
    feature_name = 'subjet3_tracks/%s' % set_type
    feature_names = {}
    #feature_names['fat_jet'] = ('pt',  'eta', 'mass')
    feature_names['subjet3_tracks'] = ('btag_ip_d0', 'btag_ip_d0_sigma', 'btag_ip_z0', 'btag_ip_z0_sigma',
                                       'chiSquared', 'deta', 'dphi', 'dr', 'eta',
                                       'numberDoF', 'numberOfInnermostPixelLayerHits',
                                       'numberOfNextToInnermostPixelLayerHits', 'numberOfPixelHits',
                                       'numberOfPixelHoles', 'numberOfPixelSharedHits', 'numberOfPixelSplitHits',
                                       'numberOfSCTHits', 'numberOfSCTHoles', 'numberOfSCTSharedHits',
                                       'pt', 'ptfrac'
                                      )
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)

def create_clusters(open_file, save_file, set_type):
    assert 1==0, "no need for this method, there are no clusters"
    category_order = ['jets', 'clusters']
    feature_name = 'clusters/%s' % set_type
    feature_names = {}
    feature_names['jets'] = ('pt',  'eta')
    feature_names['clusters'] = ('pt', 'deta', 'dphi', 'energy', 'mask')
    create_new_feature_subset(open_file, feature_name, set_type, feature_names, category_order)


def create_high(open_file, save_file, set_type):
    feature_name = 'high/%s' % set_type
    data_1 = open_file.get('hl_clusters/%s' % set_type)
    data_2 = open_file.get('hl_tracks/%s' % set_type)
    assert data_1 is not None
    assert data_2 is not None
    data = [data_1, data_2]
    merge_2_datasets(data, save_file, feature_name)


def create_low(open_file, save_file, set_type):
    assert 1==0, "no need for this method since there are no clusters"
    feature_name = 'low/%s' % set_type 
    data_1 = open_file.get('clusters/%s' % set_type)
    data_2 = open_file.get('tracks/%s' % set_type)
    assert data_1 is not None
    assert data_2 is not None
    data = [data_1, data_2]
    merge_2_datasets(data, save_file, feature_name)


def create_clusters_and_hl_clusters(open_file, save_file, set_type):
    assert 1==0, "no need for this method since there are no clusters"
    feature_name = 'clusters_and_hl_clusters/%s' % set_type
    data_1 = open_file.get('clusters/%s' % set_type)
    data_2 = open_file.get('hl_clusters/%s' % set_type)
    assert data_1 is not None
    assert data_2 is not None
    data = [data_1, data_2]
    merge_2_datasets(data, save_file, feature_name)


def create_tracks_and_hl_tracks(open_file, save_file, set_type):
    feature_name = 'tracks_and_hl_tracks/%s' % set_type
    data_1 = open_file.get('tracks/%s' % set_type)
    data_2 = open_file.get('hl_tracks/%s' % set_type)
    assert data_1 is not None
    assert data_2 is not None
    data = [data_1, data_2]
    merge_2_datasets(data, save_file, feature_name)

def create_all(open_file, save_file, set_type):
    feature_name = 'all/%s' % set_type
    data_1 = open_file.get('hl_clusters/%s' % set_type)
    data_2 = open_file.get('tracks_and_hl_tracks/%s' % set_type)
    assert data_1 is not None
    assert data_2 is not None
    data = [data_1, data_2]
    merge_2_datasets(data, save_file, feature_name)


def flatten_3d_into_2d(data):
    if len(data.shape) == 3:
        reshaped_data = data.reshape(data.shape[0], data.shape[1]*data.shape[2])
        return reshaped_data
    else:
        return data

def sub_select_data(data, start, end, sub_selection):
    if len(data.shape) == 1:
        return data[start:end]
    elif len(data.shape) == 2:
        return data[start:end, sub_selection]
    elif len(data.shape) == 3:
        return data[start:end, sub_selection, :]

def copy_in_batches(data, save_data, sub_selection):
    assert data is not None
    assert save_data is not None

    rounded_num_samples = save_data.shape[0]
    batch_size = 100
    
    if data is list:
        assert len(data) == len(sub_selection), "a sub_selection must be specified for each dataset"

    for start, end in zip(range(0, rounded_num_samples, batch_size), 
                          range(batch_size, rounded_num_samples+batch_size, batch_size)):
        if data.__class__ is list:
            assert len(data) == len(sub_selection), "a sub_selection must be specified for each dataset"
            if len(data) == 1:
                data_1 = data[0]
                sub_selection_1 = sub_selection[0]
                temp_data_1 = sub_select_data(data_1, start, end, sub_selection_1)
                temp_data_1 = flatten_3d_into_2d(temp_data_1)
                mini_batch = temp_data_1
            elif len(data) == 2:
                data_1 = data[0]
                data_2 = data[1]
                sub_selection_1 = sub_selection[0]
                sub_selection_2 = sub_selection[1]
                
                temp_data_1 = sub_select_data(data_1, start, end, sub_selection_1)
                temp_data_2 = sub_select_data(data_2, start, end, sub_selection_2)

                temp_data_1 = flatten_3d_into_2d(temp_data_1)
                temp_data_2 = flatten_3d_into_2d(temp_data_2)

                mini_batch = np.hstack((temp_data_1, temp_data_2))

            elif len(data) == 3:
                data_1 = data[0]
                data_2 = data[1]
                data_3 = data[2]
                sub_selection_1 = sub_selection[0]
                sub_selection_2 = sub_selection[1]
                sub_selection_3 = sub_selection[2]
                temp_data_1 = sub_select_data(data_1, start, end, sub_selection_1)
                temp_data_2 = sub_select_data(data_2, start, end, sub_selection_2)
                temp_data_3 = sub_select_data(data_3, start, end, sub_selection_3)
                temp_data_1 = flatten_3d_into_2d(temp_data_1)
                temp_data_2 = flatten_3d_into_2d(temp_data_2)
                temp_data_3 = flatten_3d_into_2d(temp_data_3)
                merged_1_2 = np.hstack((temp_data_1, temp_data_2))
                mini_batch = np.hstack((merged_1_2, temp_data_3))

        else:
            mini_batch = sub_select_data(data, start, end, sub_selection)
            mini_batch = flatten_3d_into_2d(mini_batch)
                
        num_dims = len(mini_batch.shape)

        if num_dims == 1:
            save_data[start:end] = mini_batch
        elif num_dims == 2:
            save_data[start:end, :] = mini_batch
        elif num_dims == 3:
            save_data[start:end, :, :] = mini_batch

if __name__ == "__main__":
    file_path = "/baldig/physicsprojects/atlas/hbb/raw_data/v_6/"
    if sys.argv[1] is None:
        assert 1==0, "Please specify a mode of processing (signal, bg, other)"

    if sys.argv[1] == 'signal':
        load_name = "temporary_flattened_shuffled_divided_data_signal.h5"
        #save_name = "categorized_data_signal.h5"
        save_name = "categorized_data_divided_signal.h5"
    elif sys.argv[1] == 'bg':
        load_name = "temporary_flattened_shuffled_divided_data_bg.h5"
        #save_name = "categorized_data_bg.h5"
        save_name = "categorized_data_divided_bg.h5"
    elif sys.argv[1] == 'top':
        load_name = "temporary_flattened_shuffled_divided_data_top.h5"
        #save_name = "categorized_data_top.h5"
        save_name = "categorized_data_divided_top.h5"
    elif sys.argv[1] == 'test':
        load_name = "temporary_flattened_shuffled_divided_data_signal.h5"
        save_name = "delete_me_categorized_data_signal_test_valid_train.h5"
        if sys.argv[2] == 'signal':
            load_name = "temporary_flattened_shuffled_divided_data_signal.h5"
            save_name = "delete_me_categorized_data_signal.h5"
        elif sys.argv[2] == 'bg':
            load_name = "temporary_flattened_shuffled_divided_data_bg.h5"
            save_name = "delete_me_categorized_data_bg.h5"
        else:
            pass   
    elif sys.argv[1] == 'hl_tracks':
        load_name = "temporary_flattened_shuffled_divided_data_signal.h5"
        #load_name = "temporary_flattened_shuffled_divided_data_bg.h5"
        save_name = "categorized_data_signal_test_valid_train.h5"
    elif sys.argv[1] == 'other':
        load_name = "temporary_flattened_shuffled_divided_data_%s.h5" % 'other'
        save_name = "categorized_data_%s_test_valid_train.h5" % 'other'
    else:
        assert 1==0, "please specify signal or bg"

    hf = h5py.File(file_path + load_name, 'r')
    save_file = h5py.File(file_path + save_name, 'a')
    print(hf.keys())
    if sys.argv[1] == 'test' or sys.argv[1] == 'hl_tracks':
        for set_type in ['test', 'valid', 'train']:
            print(set_type)
            #print("splitting tracks")
            #create_tracks(hf, save_file, set_type)
            #print("splitting hl tracks")
            #create_high_level_tracks(hf, save_file, set_type)
            #print("Splitting hl clusters")
            #create_high_level_clusters(hf, save_file, set_type)
            #print("splitting high")
            #create_high(save_file, save_file, set_type)
            print("splitting mv2c10+")
            create_mv2c10_plus(hf, save_file, set_type)
            #print("creating single_jet_predictions")
            #create_single_jet_predictions(hf, save_file, set_type)
        assert 1==0
    
    for set_type in ['valid', 'test', 'train']:
        print(set_type)
        print("Splitting weights")
        create_weights(hf, save_file, set_type)
        print("Splitting fat_jet")
        create_fat_jet(hf, save_file, set_type)
        print("Splitting subjet1")
        create_subjet1(hf, save_file, set_type)
        print("Splitting subjet2")
        create_subjet2(hf, save_file, set_type)
        print("Splitting subjet3")
        create_subjet3(hf, save_file, set_type)
        print("Splitting subjet1_tracks")
        create_subjet1_tracks(hf, save_file, set_type)
        print("Splitting subjet2_tracks")
        create_subjet2_tracks(hf, save_file, set_type)
        print("Splitting subjet3_tracks")
        create_subjet3_tracks(hf, save_file, set_type)
        print("Splitting hl clusters")
        create_high_level_clusters(hf, save_file, set_type)
        print("splitting hl tracks")
        create_high_level_tracks(hf, save_file, set_type)
        print("splitting mv2c10")
        create_mv2c10(hf, save_file, set_type)
        print("splitting tracks")
        create_tracks(hf, save_file, set_type)
        print("splitting mv2c10+")
        create_mv2c10_plus(hf, save_file, set_type)
        #print("splitting clusters")
        #create_clusters(hf, save_file, set_type)
        print("splitting high")
        create_high(save_file, save_file, set_type)
        #print("splitting low")
        #create_low(save_file, save_file, set_type)
        #print("splitting clusters_and_hl_clusters")
        #create_clusters_and_hl_clusters(save_file, save_file, set_type)
        print("splitting tracks_and_hl_tracks")
        create_tracks_and_hl_tracks(save_file, save_file, set_type)
        print("splitting all")
        create_all(save_file, save_file, set_type)
        print("splitting DL1")
        create_DL1(save_file, save_file, set_type)
