import sys
import numpy as np
from tqdm import trange

from tensorflow.keras.layers import Add, Dense, Input, LeakyReLU
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import plot_model, Sequence
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow import __version__ as tf_version
import tensorflow as tf
import matplotlib.pyplot as plt
import datetime
import os
from random import randrange, shuffle
import time
import pickle

print('tensorflow version', tf_version)

from pattern import *

# param
N_BATCHES = 14500
N_TEST_DATA = 8192 * 100
n_layer_nodes = [64 for _ in range(4)]
INITIAL_EPOCH = 0

# const
N_PHASE = 30
N_MEMORY_DATA = 5000

# train param
N_EPOCHS = 150
BATCH_SIZE = 8192
#EARLY_STOP_PATIENCE = 30


# pre calculation
def fill0(num, n_digits):
    return '0' * (n_digits - len(str(num))) + str(num)
now = datetime.datetime.today()
date_str = str(now.year) + fill0(now.month, 2) + fill0(now.day, 2) + '_' + fill0(now.hour, 2) + fill0(now.minute, 2)
N_TRAIN_DATA = N_BATCHES * BATCH_SIZE
N_DATA = N_TRAIN_DATA + N_TEST_DATA
print('train', N_TRAIN_DATA, 'test', N_TEST_DATA, 'overall', N_DATA)





# model

xs = []
ys = []
for name, n_input_nodes, n_symmetry, _, _, _ in pattern_info:
    layers = []
    for i in range(len(n_layer_nodes)):
        layers.append(Dense(n_layer_nodes[i], name=name + '_dense_' + str(i)))
        layers.append(LeakyReLU(alpha=0.01))
    layers.append(Dense(1, name=name + '_out'))
    for i in range(n_symmetry):
        x = Input(shape=n_input_nodes + 1, name=name + '_in_' + str(i), dtype='float16')
        xs.append(x)
        y = x
        for layer in layers:
            y = layer(y)
        ys.append(y)
y_all = Add(name='add')(ys)
model = Model(inputs=xs, outputs=y_all)
#model.summary()
plot_model(model, to_file='./../model/model.png', show_shapes=True)
model.compile(loss='mse', metrics='mae', optimizer='adam')

print('param', model.count_params())
with open('./../model/log.txt', 'a') as f:
    f.write(date_str + ' layers: ' + str(n_layer_nodes) + ' params: ' + str(model.count_params()) + ' n_train_data ' + str(N_TRAIN_DATA) + ' n_test_data ' + str(N_TEST_DATA) + '\n')


# test data
print('getting test data...')
with open('./../train_data/bin_data/20230729_pickle_8192/val_data_14509_14609.pkl', 'rb') as f:
    test_data = pickle.load(f)
print('getting test labels...')
with open('./../train_data/bin_data/20230729_pickle_8192/val_labels_14509_14609.pkl', 'rb') as f:
    test_labels = pickle.load(f)
print('n_test_data', len(test_labels))

# train data
train_data = []
train_labels = []
print('getting train data on memory...')
for i in trange(N_MEMORY_DATA):
    with open('./../train_data/bin_data/20230729_pickle_8192/' + str(i) + '_data.pkl', 'rb') as f:
        data = pickle.load(f)
    with open('./../train_data/bin_data/20230729_pickle_8192/' + str(i) + '_labels.pkl', 'rb') as f:
        labels = pickle.load(f)
    train_data.append(data)
    train_labels.append(labels)

# dataset generator
class DatasetGenerator(tf.keras.utils.Sequence):
    def __init__(self):
        return

    def __getitem__(self, idx):
        shuffled_idx = idx
        if shuffled_idx < N_MEMORY_DATA:
            return train_data[shuffled_idx], train_labels[shuffled_idx]
        with open('./../train_data/bin_data/20230729_pickle_8192/' + str(shuffled_idx) + '_data.pkl', 'rb') as f:
            data = pickle.load(f)
        with open('./../train_data/bin_data/20230729_pickle_8192/' + str(shuffled_idx) + '_labels.pkl', 'rb') as f:
            labels = pickle.load(f)
        return data, labels

    def on_epoch_end(self):
        return

    def __len__(self):
        return N_BATCHES



# train
#early_stop = EarlyStopping(monitor='val_loss', patience=EARLY_STOP_PATIENCE)
model_checkpoint = ModelCheckpoint(filepath=os.path.join('./../model/', 'model_{epoch:02d}_{loss:.4f}_{mae:.4f}_{val_loss:.4f}_{val_mae:.4f}.h5'), monitor='val_loss', verbose=1, period=1)
#reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=0.0001)
history = model.fit(DatasetGenerator(), initial_epoch=INITIAL_EPOCH, epochs=N_EPOCHS, batch_size=BATCH_SIZE, workers=1, use_multiprocessing=False, shuffle=True, callbacks=[model_checkpoint], validation_data=(test_data, test_labels))

model.save('./../model/model.h5')

cut_epoch = 0

for key in ['loss', 'val_loss']:
    plt.plot(history.history[key][cut_epoch:], label=key)
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(loc='best')
plt.savefig('./../model/loss.png')
plt.clf()

for key in ['mae', 'val_mae']:
    plt.plot(history.history[key][cut_epoch:], label=key)
plt.xlabel('epoch')
plt.ylabel('mae')
plt.legend(loc='best')
plt.savefig('./../model/mae.png')
plt.clf()

with open('./../model/log.txt', 'a') as f:
    f.write('single big data' + '\t' + date_str + '\t' + str(model.count_params()) + '\t' + str(N_DATA) + '\t' + str(len(history.history['loss'])) + '\t' + str(history.history['loss'][-1]) + '\t' + str(history.history['val_loss'][-1]) + '\t' + str(history.history['mae'][-1]) + '\t' + str(history.history['val_mae'][-1]) + '\n')
