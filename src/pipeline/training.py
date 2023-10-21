from src import logger, customException
import tensorflow as tf
from src.utils import loadObject, saveObject
from dataclasses import dataclass  
import os
from src.components.data_transformation import DataTransformation
import sys
from src.utils import getPredictions, getMetrics

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
            hist = model.fit(train, epochs=self.trainerConfig.EPOCHS, validation_data=val, callbacks=[tensorboardCallback])

            # Saving the model as .h5 to ensure it can be reused across different runtimes.
            model.save('artifacts/trained_model.h5')
            logger.info('Saved Trained Model')

            y_true, y_pred = getPredictions(model, test)
            accuracy, precision, recall, f1 = getMetrics(y_true, y_pred)
            logger.info(f'''The model gives the following metrics on the test dataset: 
                        Accuracy: {accuracy}
                        Precision: {precision}
                        Recall: {recall}
                        F1 Score: {f1}
                        ''')
        
        except Exception as e:
            raise customException(e, sys)

if __name__=="__main__":
    trainer = ModelTrainer()
    trainer.initiateTraining()