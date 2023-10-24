from flask import Flask, request
from src.pipeline.prediction import FlaskPredictionPipeline, imageFile
from src.utils import loadObject
from src import logger

model = loadObject('artifacts/MLFlow_model.pkl')
logger.info('Loaded Model')

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Blood Cancer App'

@app.route('/predict', methods=['POST'])
def predict():
    
    image = request.files['file'].stream
    imgObj = imageFile(image)
    arr = imgObj.getArr()

    logger.info('Initiating Prediction Pipeline')
    predictObj = FlaskPredictionPipeline(model)
    className, confidence = predictObj.predict(arr)

    return {
        'Class': className,
        'Confidence': confidence
    }

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)