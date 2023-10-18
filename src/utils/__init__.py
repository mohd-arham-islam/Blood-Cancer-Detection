import dill
import os
import sys 
from src import customException

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