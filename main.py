from model.creat_model import create
import tensorflow as tf
import time
from keras.callbacks import History

import random
import numpy as np

from data.format_data import load_data
from model.evaluate import evaluate
history = History()
def set_seeds(seed):
    np.random.seed(seed)
    random.seed(seed)
    tf.random.set_seed(seed)
    
def train(model, x_train, y_train, bz, e):
    print(type(x_train), type(y_train))
    print(x_train.shape)
    print(y_train.shape)
    model.fit(x_train, y_train, epochs=e,validation_split=0.2,
                        verbose=1, batch_size=bz,callbacks=[history])
    

    
def main(mode):
    set_seeds(0)
    model = create()
    x_train , y_train, x_test, x_valid, y_test, y_valid = load_data()
    if mode == "train":
        train(model, x_train, y_train,256, 30)
        name = str(time.time()) + ".h5"
        model.save(name)
        path = name
        evaluate(x_test, y_test, model, path, history)
    if mode == "evaluate":
        evaluate(x_test, y_test, model, './model/best.h5')
    



main("train")
    
    