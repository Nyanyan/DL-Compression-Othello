import sys
from tensorflow.keras.models import load_model, Model
import numpy as np

from pattern import *

file = './../model/model.h5'

STEP = 128
N_PHASE = 30
BATCH_SIZE = 4096

# load model

all_model = load_model(file)
model = Model(inputs=all_model.input, outputs=all_model.get_layer('add').input)


# create data

N_MAX_DATA = 65536
all_data = []
for _, n_input_nodes, n_symmetry, _, _, _ in pattern_info:
    for _ in range(n_symmetry):
        all_data.append(np.zeros((N_MAX_DATA, n_input_nodes + 1), dtype=np.float16))

feature_idx = 0
for name, n_input_nodes, n_symmetry, normalize, n_variables, _ in pattern_info[:16]:
    for idx in range(n_variables):
        for i in range(n_input_nodes // 2):
            digit = (idx // (3 ** (n_input_nodes // 2 - 1 - i))) % 3
            if digit == 0: # player
                all_data[feature_idx][idx][i] = 1 / normalize
            elif digit == 1: # opponent
                all_data[feature_idx][idx][i + n_input_nodes // 2] = 1 / normalize
    feature_idx += n_symmetry

for name, n_input_nodes, n_symmetry, normalize, n_variables, _ in pattern_info[16:16+3]:
    for idx in range(n_variables):
        p = (idx // normalize) / normalize
        o = (idx % normalize) / normalize
        all_data[feature_idx][idx][0] = p
        all_data[feature_idx][idx][1] = o
    feature_idx += n_symmetry

for name, n_input_nodes, n_symmetry, normalize, n_variables, _ in pattern_info[16+3:]:
    for idx in range(n_variables):
        for i in range(n_input_nodes):
            all_data[feature_idx][idx][i] = (1 & (idx >> (n_input_nodes - 1 - i))) / normalize
    feature_idx += n_symmetry



# predict

for phase in range(30):
    print(phase)

    feature_idx = 0
    for _, n_input_nodes, n_symmetry, _, n_variables, _ in pattern_info:
        for idx in range(n_variables):
            all_data[feature_idx][idx][n_input_nodes] = phase / N_PHASE
        feature_idx += n_symmetry

    prediction = model.predict(all_data, batch_size=BATCH_SIZE)

    out_file = './../model/' + str(phase) + '.txt'
    with open(out_file, 'w') as f:
        feature_idx = 0
        for name, n_input_nodes, n_symmetry, normalize, n_variables, _ in pattern_info:
            for idx in range(n_variables):
                v = round(prediction[feature_idx][idx][0] * STEP)
                f.write(str(v) + '\n')
            feature_idx += n_symmetry
