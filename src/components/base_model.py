import os
import sys
from dataclasses import dataclass
import tensorflow as tf
from tensorflow import keras
from keras.models import Model
from keras.layers import Input, Dense, GlobalMaxPooling2D, Dropout, Rescaling, Resizing
from keras.applications import VGG16

from src import logger, customException
from src.utils import saveObject

@dataclass()
class BaseModelConfig:
    modelPath = os.path.join('artifacts', 'base_model.pkl')

class BaseModel:
    def __init__(self):
        self.modelConfig = BaseModelConfig()
    
    def createModel(self):
        try:
            inputLayer = Resizing(height=224, width=224)(Input(shape=(224,224,3)))
            inputLayer = Rescaling(1./255)(inputLayer)

            vgg = VGG16(include_top=False, weights='imagenet')
            for layer in vgg.layers:
                layer.trainable=False
            logger.info('Downloaded VGG-16 Model')
            
            vgg = vgg(inputLayer)
            maxPooling = GlobalMaxPooling2D()(vgg)
            firstLayer = Dense(256, activation='relu')(maxPooling)
            secondLayer = Dense(128, activation='sigmoid')(firstLayer)
            dropout = Dropout(0.25)(secondLayer)

            thirdLayer = Dense(64, activation='sigmoid')(dropout)
            fourthLayer = Dense(16, activation='sigmoid')(thirdLayer)
            fifthLayer = Dense(8, activation='sigmoid')(fourthLayer)
            finalLayer = Dense(4, activation='softmax')(fifthLayer)

            model = Model(inputs=inputLayer, outputs=finalLayer)
            logger.info(f'Created model with configurations: \n{model.summary()}')

            saveObject(filePath=self.modelConfig.modelPath, object=model)
            logger.info(f'Saved Base Model at {self.modelConfig.modelPath}')
        
        except Exception as e:
            raise customException(e, sys)
    
if __name__=="__main__":
    modelBuilder = BaseModel()
    modelBuilder.createModel()