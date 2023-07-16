
from keras.callbacks import History
import pandas as pd
import ast
import numpy as np
from sklearn.model_selection import train_test_split
history = History()
def load_data():
    
    df = pd.read_csv('data/data.csv')
    df['embedding'] = df['embedding'].apply(ast.literal_eval)
    max_length = max(df['embedding'].apply(len))
    df['embedding'] = df['embedding'].apply(lambda x: x + [0] * (max_length - len(x)))
    embedding_matrix = np.array(df['embedding'].tolist())
    
    # MODIFIED 
    data = embedding_matrix.reshape((len(embedding_matrix), 60, 4, 1))  # reshape data to be (samples, height, width, channels)
    DNA = data
    
    
    oneIn = np.array(df['oneInsertion'].tolist())
    oneD = np.array(df['oneDeletion'].tolist())
    dele = np.array(df['deletions'].tolist())
    l = []
    for i in range(len(dele)):
        temp = [dele[i], oneIn[i], oneD[i]]
        l.append(temp)
    labels = np.array(l)
        
    
    
    
    
    x_train, x_test, y_train, y_test = train_test_split(DNA, labels, test_size = 0.20, random_state = 0)
    x_test, x_valid, y_test, y_valid = train_test_split(x_test, y_test, test_size = 0.5, random_state = 0)
    return x_train , y_train, x_test, x_valid, y_test, y_valid 