import dill
import os
import sys 
from src import customException
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

def saveObject(filePath, object):
    try:
        dirPath = os.path.dirname(filePath)
        os.makedirs(dirPath, exist_ok=True)

        with open(filePath, "wb") as fileObj:
            dill.dump(object, fileObj)
        
    except Exception as e:
        raise customException(e, sys)
    
def loadObject(filePath):
    try:
        with open(filePath, 'rb') as file:
            return dill.load(file)
    except Exception as e:
        raise customException(e, sys)
    
def getPredictions(model, test):
    try:
        y_true, y_pred = [], []
        for i in range(len(test)):
            arr = test.as_numpy_iterator().next()
            y_true.append(list(arr[1]))
            prediction = model.predict(arr[0])
            for j in range(16):
                y_pred.append(np.argmax(prediction[j]))
        
        y_pred = np.array(y_pred)
        y_true = np.array(y_true)
        y_true = y_true.reshape(320, )

        return (
            y_true,
            y_pred
        )
    except Exception as e:
        raise customException(e, sys)

def getMetrics(y_true, y_pred):
    try:
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='macro')
        recall = recall_score(y_true, y_pred, average='macro')
        f1 = f1_score(y_true, y_pred, average='macro')

        return {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1
        }
    except Exception as e:
        raise customException(e, sys)

def getBatchSize(data):
    try:
        totalSize = len(data)
        trainSize = int(totalSize*0.7)
        valSize = int(totalSize*0.2)
        testSize = totalSize - trainSize - valSize
        return (
            trainSize,
            valSize,
            testSize
        )
    except Exception as e:
        raise customException(e, sys)