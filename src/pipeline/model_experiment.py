import os
import sys
from src import customException, logger
from src.pipeline.training import ModelTrainer
from dotenv import load_dotenv
from dataclasses import dataclass
import mlflow
from mlflow.models.signature import infer_signature

load_dotenv()

@dataclass()
class ExperimentConfig:
    MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
    MLFLOW_TRACKING_USERNAME = os.getenv('MLFLOW_TRACKING_USERNAME')
    MLFLOW_TRACKING_PASSWORD = os.getenv('MLFLOW_TRACKING_PASSWORD')

class ModelExperiment:
    def __init__(self):
        self.experimentConfig = ExperimentConfig()
    
    def newExperiment(self, expName, runName, batchSize, EPOCHS, optimizer):
        try:
            trainer = ModelTrainer()
            model, accuracy, precision, recall, f1, input, output = trainer.initiateTraining(batchSize=batchSize, EPOCHS=EPOCHS, optimizer=optimizer)
            logger.info('Model Training complete')

            modelSignature = infer_signature(input, output)
            mlflow.set_experiment(expName)

            with mlflow.start_run(run_name=runName):
                mlflow.log_param('Batch Size', batchSize)
                mlflow.log_param('Epochs', EPOCHS)

                mlflow.log_metric('Accuracy', accuracy)
                mlflow.log_metric('Precision', precision)
                mlflow.log_metric('Recall', recall)
                mlflow.log_metric('F1 Score', f1)

                mlflow.tensorflow.log_model(model, "cnn", signature=modelSignature)
            mlflow.end_run()
        
        except Exception as e:
            raise customException(e, sys)

if __name__=="__main__":
    experiment = ModelExperiment()
    experiment.newExperiment(
        'VGGModel',
        'Run-1',
        32,
        15,
        'adam'
    )