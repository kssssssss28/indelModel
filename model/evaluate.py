from keras.callbacks import ReduceLROnPlateau, EarlyStopping
import tensorflow as tf
import pandas as pd
import ast
from sklearn.model_selection import KFold
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from sklearn.metrics import r2_score
from scipy.stats import kendalltau

def evaluate(x_test, y_test, model, path, history):
    y_pred = model.predict(x_test)
    r2 = r2_score(y_test, y_pred)
    y_pred = np.squeeze(y_pred) 
    y_pred_dele = []
    y_pred_oneI = []
    y_pred_oneD = []
    y_test_dele = []
    y_test_oneI= []
    y_test_oneD= []
    for i in range(len(y_pred)):
        y_pred_dele.append(y_pred[i][0])
        y_pred_oneI.append(y_pred[i][1])
        y_pred_oneD.append(y_pred[i][2])
        y_test_dele.append(y_test[i][0])
        y_test_oneI.append(y_test[i][1])
        y_test_oneD.append(y_test[i][2])
        
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend(['Training', 'Validation'])
    plt.show()

    
    
    print("--- run five fold cross validation ----")
    five_fold_cross_validation(path, 256)
    
    
    
def five_fold_cross_validation(model_path, bz):
    df = pd.read_csv('data/data.csv')
    df['embedding'] = df['embedding'].apply(ast.literal_eval)
    max_length = max(df['embedding'].apply(len))
    df['embedding'] = df['embedding'].apply(lambda x: x + [0] * (max_length - len(x)))
    embedding_matrix = np.array(df['embedding'].tolist())
    data = embedding_matrix.reshape((len(embedding_matrix), 60, 4, 1))
    DNA = data
    oneIn = np.array(df['oneInsertion'].tolist())
    oneD = np.array(df['oneDeletion'].tolist())
    dele = np.array(df['deletions'].tolist())
    l = []
    for i in range(len(dele)):
        temp = [dele[i], oneIn[i], oneD[i]]
        l.append(temp)
    labels = np.array(l)

    kf = KFold(n_splits=5, shuffle=True, random_state=0)

    r2_scores = []
    tau_insertion = []
    tau_deletion = []
    pearson_deletion = []

    for train_index, test_index in kf.split(DNA):
        x_train, x_test = DNA[train_index], DNA[test_index]
        y_train, y_test = labels[train_index], labels[test_index]

        x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2, random_state=0)
        model = tf.keras.models.load_model(model_path)

        y_pred = model.predict(x_test)
        r2 = r2_score(y_test, y_pred)
        r2_scores.append(r2)

        y_pred_dele = []
        y_pred_oneI = []
        y_pred_oneD = []
        y_test_dele = []
        y_test_oneI = []
        y_test_oneD = []
        for i in range(len(y_pred)):
            y_pred_dele.append(y_pred[i][0])
            y_pred_oneI.append(y_pred[i][1])
            y_pred_oneD.append(y_pred[i][2])
            y_test_dele.append(y_test[i][0])
            y_test_oneI.append(y_test[i][1])
            y_test_oneD.append(y_test[i][2])

        tau_i, _ = kendalltau(y_test_oneI, y_pred_oneI)
        tau_d, _ = kendalltau(y_test_oneD, y_pred_oneD)
        pearson_d = np.corrcoef(y_test_dele, y_pred_dele)[0, 1]

        tau_insertion.append(tau_i)
        tau_deletion.append(tau_d)
        pearson_deletion.append(pearson_d)

    print("R2 Score:", np.mean(r2_scores))
    print("Mean Kendall's Tau (1bp insertion):", np.mean(tau_insertion))
    print("Mean Kendall's Tau (1bp deletion):", np.mean(tau_deletion))
    print("Mean Pearson's Correlation (deletion freq):", np.mean(pearson_deletion))

