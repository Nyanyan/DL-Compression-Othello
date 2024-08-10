import sys
import numpy as np
from tqdm import trange
import pickle
import os

from pattern import *

BATCH_SIZE = 8192 #16384
N_PHASE = 30
TEST_N_BATCH = 100

all_data = []
for _, n_input_nodes, n_symmetry, _, _, _ in pattern_info:
    for _ in range(n_symmetry):
        all_data.append(np.zeros((BATCH_SIZE, n_input_nodes + 1), dtype=np.float16))
all_labels = np.zeros(BATCH_SIZE)

def to_pickle(data_idx, file_idx, n_data):
    file = './../train_data/bin_data/20230729_dnn_8192/' + str(file_idx) + '.dat'
    #print(file)
    with open(file, 'br') as f:
        for _ in range(n_data):
            phase = int.from_bytes(f.read(1), sys.byteorder)
            feature_idx = 0
            for _, n_input_nodes, n_symmetry, normalize, _, feature_type in pattern_info:
                for _ in range(n_symmetry):
                    if feature_type == 'disc_pattern':
                        bits = int.from_bytes(f.read(3), sys.byteorder)
                        for i in range(n_input_nodes):
                            all_data[feature_idx][data_idx][i] = (1 & (bits >> (23 - i)))
                    elif feature_type == 'additional_feature':
                        for i in range(n_input_nodes):
                            all_data[feature_idx][data_idx][i] = int.from_bytes(f.read(1), sys.byteorder) / normalize
                    elif feature_type == 'mobility_pattern':
                        bits = int.from_bytes(f.read(2), sys.byteorder)
                        for i in range(n_input_nodes):
                            all_data[feature_idx][data_idx][i] = (1 & (bits >> (15 - i)))
                    else:
                        print('ERR got', feature_type)
                    all_data[feature_idx][data_idx][n_input_nodes] = phase / N_PHASE # input phase
                    feature_idx += 1
            all_labels[data_idx] = int.from_bytes(f.read(1), sys.byteorder) - 64 # / 64
            data_idx += 1

# test data generation

all_data = []
for _, n_input_nodes, n_symmetry, _, _, _ in pattern_info:
    for _ in range(n_symmetry):
        all_data.append(np.zeros((BATCH_SIZE * TEST_N_BATCH, n_input_nodes + 1), dtype=np.float16))
all_labels = np.zeros(BATCH_SIZE * TEST_N_BATCH)

N_ALL_DATA_PER_8192 = 14609
TEST_FILE_START = N_ALL_DATA_PER_8192 - TEST_N_BATCH
print('test', TEST_FILE_START, 'to', N_ALL_DATA_PER_8192)
didx = 0
for file_idx in trange(TEST_FILE_START, N_ALL_DATA_PER_8192):
    to_pickle(didx, file_idx, BATCH_SIZE)
    didx += BATCH_SIZE
pkl_file = './../train_data/bin_data/20230729_pickle_8192/val_data_' + str(TEST_FILE_START) + '_' + str(N_ALL_DATA_PER_8192) + '.pkl'
#print(pkl_file)
with open(pkl_file, 'wb') as f:
    pickle.dump(all_data, f)
pkl_file = './../train_data/bin_data/20230729_pickle_8192/val_labels_' + str(TEST_FILE_START) + '_' + str(N_ALL_DATA_PER_8192) + '.pkl'
#print(pkl_file)
with open(pkl_file, 'wb') as f:
    pickle.dump(all_labels, f)
