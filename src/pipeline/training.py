from src import logger, customException
import tensorflow as tf
from src.utils import loadObject, saveObject
from dataclasses import dataclass  
import os
from src.components.data_transformation import DataTransformation
import sys

@dataclass()
class ModelTrainerConfig:
    trainedModelPath = os.path.join('artifacts', 'trained_model.pkl')
    baseModelPath = os.path.join('artifacts', 'base_model.pkl')
    EPOCHS = 20
    modelLogDir = os.path.join('Model logs')

    optimizer = 'adam'
    loss = tf.keras.losses.SparseCategoricalCrossentropy()
    metrics = ['accuracy']

class ModelTrainer:
    def __init__(self):
        self.trainerConfig = ModelTrainerConfig()
    
    def initiateTraining(self):
        try:
            # Loading the splitted data
            transformer = DataTransformation()
            train, val, test = transformer.initiateTransformation()
            logger.info('Loaded the dataset')

            # Loading the model
            model = loadObject(self.trainerConfig.baseModelPath)
            logger.info('Loaded the base model. Initiating training')

            logDir = self.trainerConfig.modelLogDir
            os.makedirs(logDir, exist_ok=True)

            model.compile(
                optimizer=self.trainerConfig.optimizer,
                loss=self.trainerConfig.loss,
                metrics=self.trainerConfig.metrics
            )

            tensorboardCallback = tf.keras.callbacks.TensorBoard(log_dir=logDir)
            hist = model.fit(train, epochs=20, validation_data=val, callbacks=[tensorboardCallback])

            saveObject(
                filePath=self.trainerConfig.trainedModelPath, 
                object=model
                )
            logger.info('Saved Trained Model')
        
        except Exception as e:
            raise customException(e, sys)

if __name__=="__main__":
    trainer = ModelTrainer()
    trainer.initiateTraining()