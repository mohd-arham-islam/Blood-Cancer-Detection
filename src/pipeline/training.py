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
    modelLogDir = os.path.join('Model logs')

    loss = tf.keras.losses.SparseCategoricalCrossentropy()
    metrics = ['accuracy']

class ModelTrainer:
    def __init__(self):
        self.trainerConfig = ModelTrainerConfig()
    
    def initiateTraining(self, batchSize, EPOCHS, optimizer):
        try:
            # Loading the splitted data
            transformer = DataTransformation()
            train, val, test = transformer.initiateTransformation(batchSize)
            logger.info('Loaded the dataset')

            # Loading the model
            model = loadObject(self.trainerConfig.baseModelPath)
            logger.info('Loaded the base model. Initiating training')

            logDir = self.trainerConfig.modelLogDir
            os.makedirs(logDir, exist_ok=True)

            model.compile(
                optimizer=optimizer,
                loss=self.trainerConfig.loss,
                metrics=self.trainerConfig.metrics
            )

            tensorboardCallback = tf.keras.callbacks.TensorBoard(log_dir=logDir)
            hist = model.fit(train, epochs=EPOCHS, batch_size=batchSize, validation_data=val, callbacks=[tensorboardCallback])

            # Saving the model as .h5 to ensure it can be reused across different runtimes.
            # model.save('artifacts/trained_model.h5')
            # logger.info('Saved Trained Model')

            y_true, y_pred = getPredictions(model, test, batchSize)
            metrics = getMetrics(y_true, y_pred)
            accuracy, precision, recall, f1 = metrics['Accuracy'], metrics['Precision'], metrics['Recall'], metrics['F1 Score']

            pred = model.predict(test)
            
            return (
                model,
                accuracy,
                precision,
                recall,
                f1,
                test.as_numpy_iterator().next()[0],   # This will be used to create model signature during experiment tracking.
                pred
            )
        
        except Exception as e:
            raise customException(e, sys)

if __name__=="__main__":
    trainer = ModelTrainer()
    trainer.initiateTraining(batchSize=16, EPOCHS=20, optimizer='adam')