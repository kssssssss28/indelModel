from keras.callbacks import ReduceLROnPlateau, EarlyStopping
import tensorflow as tf
import time
from keras.callbacks import History
history = History()
import torch
import pandas as pd
import ast
from keras.layers import Dropout
import random
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras import backend as K
from sklearn.metrics import r2_score, mean_squared_error
from scipy.stats import kendalltau
from keras.callbacks import TensorBoard, Callback
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Bidirectional, Reshape
def create():
    model = Sequential()
    filters = 256
    kernel_size = (3, 3) 
    input_shape = (60,4, 1) 
    model.add(Conv2D(filters, kernel_size, input_shape=input_shape,))
    model.add(Conv2D(filters, (2, 2), input_shape=input_shape)) 
    model.add(Flatten())
    model.add(Dense(100, activation='tanh'))
    model.add(Dense(100, activation='tanh'))
    model.add(Dense(100, activation='tanh'))
    model.add(Dense(3)) 
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
    return model