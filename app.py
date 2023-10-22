from flask import Flask, request
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.utils import img_to_array
import requests
from PIL import Image
from io import BytesIO
from src.utils import loadObject

model = tf.keras.models.load_model('artifacts/trained_model.h5')

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Arham Islam'

@app.route('/predict', methods=['POST'])
def predict():
    
    image = request.files['file'].stream
    pil_image = Image.open(image)
    resizedImg = pil_image.resize((224, 224))
    
    arr = np.array(resizedImg)
    # arr = arr / 255.0
    batchedImg = np.expand_dims(arr, 0)
    prediction = model.predict(batchedImg)[0]
    classNames = ['Benign', 'Early', 'Pre', 'Pro']
    pos = np.argmax(prediction)
    # image = image/255.0
    # img = Image.open(image)
    # img = img.resize((224, 224))
    # img = img_to_array(img)/255.0
    # img = img.reshape(1, 224, 224, 3)
    return {
        'Class': classNames[pos],
        'Confidence': round(prediction[pos]*100, 1)
    }

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)