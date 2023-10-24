import os
import sys
from src import logger, customException
import numpy as np
from PIL import Image
from dataclasses import dataclass
from src.utils import loadObject

classNames = ['Benign', 'Early', 'Pre', 'Pro']

@dataclass()
class PredictionConfig:
    modelPath = os.path.join('artifacts/MLFlow_model.pkl')

class imageFile:
    def __init__(self, file):
        self.file = file
    
    def getArr(self):
        try:
            pilImg = Image.open(self.file)
            pilImg = pilImg.resize((224, 224))
            arr = np.array(pilImg)

            return arr
        
        except Exception as e:
            raise customException(e, sys)
        
class PredictionPipeline:
    def __init__(self):
        self.predictionConfig = PredictionConfig()

    def predict(self, arr):
        modelPath = self.predictionConfig.modelPath
        model = loadObject(filePath=modelPath)
        logger.info('Loaded Model')

        batchedImg = np.expand_dims(arr, 0)
        batchedImg = batchedImg.astype('float32')
        logger.info('Created batched image')

        prediction = model.predict(batchedImg)[0]
        logger.info('Prediction Complete')

        classNames = ['Benign', 'Early', 'Pre', 'Pro']
        pos = np.argmax(prediction)

        className = classNames[pos]
        confidence = round(prediction[pos]*100, 1)

        return (
            className,
            confidence
        )

# Pipeline for the flask app to ensure the API request does not time out.
class FlaskPredictionPipeline:
    def __init__(self, model):
        self.model = model

    def predict(self, arr):

        batchedImg = np.expand_dims(arr, 0)
        batchedImg = batchedImg.astype('float32')
        logger.info('Created batched image')

        prediction = self.model.predict(batchedImg)[0]
        logger.info('Prediction Complete')

        classNames = ['Benign', 'Early', 'Pre', 'Pro']
        pos = np.argmax(prediction)

        className = classNames[pos]
        confidence = round(prediction[pos]*100, 1)

        return (
            className,
            confidence
        )