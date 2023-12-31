import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image_dataset_from_directory
import os
import sys
from src import logger, customException
from dataclasses import dataclass
from src.utils import getBatchSize

@dataclass()
class DataTransformationConfig:
    dataDir = os.path.join('artifacts', 'images')
    imageSize = (224,224)


class DataTransformation:
    def __init__(self):
        self.transformationConfig = DataTransformationConfig()
    
    def initiateTransformation(self, batchSize):
        try:
            logger.info('Splitting the data into training, validation, and test sets')

            dataDir = self.transformationConfig.dataDir
            imageSize = self.transformationConfig.imageSize

            data = image_dataset_from_directory(
                dataDir,
                image_size=imageSize,
                batch_size=batchSize
            )

            logger.info('Successfully read images from directory.')

            trainSize, testSize, valSize = getBatchSize(data)

            train = data.take(trainSize)
            val = data.skip(trainSize).take(valSize)
            test = data.skip(trainSize+valSize).take(testSize)

            logger.info('Splitted the dataset successfully')

            return (
                train,
                val,
                test
            )
        
        except Exception as e:
            raise customException(e, sys)
        