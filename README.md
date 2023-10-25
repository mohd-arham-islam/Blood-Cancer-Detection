# Analyzing Peripheral Blood Smear (PBS) images to detect Acute Lymphoblastic Leukemia
## Introduction
Acute lymphoblastic leukemia (ALL) is a type of cancer that affects the blood and bone marrow. It is characterized by the overproduction of immature white blood cells called lymphoblasts. ALL is the most common childhood cancer. It occurs when a bone marrow cell develops errors in its DNA.

This project analyzes **Peripheral Blood Smear** (PBS) images to to detect and classify 4 stages of **Acute Lymphoblastic Leukemia** - **Benign (Normal Stage)**, **Malignant Early**, **Malignant Pre**, and **Malignant Pro** stages.

The dataset we used was put together by a group of researchers, and I'm thankful for their work. It has around 3,000 PBS images, divided into four categories. The dataset is neatly organized, with separate folders for each category, and the images have easy-to-understand names.

Link to the research paper: https://onlinelibrary.wiley.com/doi/10.1002/int.22753

Link to the dataset: https://www.kaggle.com/datasets/mehradaria/leukemia


## Data Ingestion
To make the project a bit more challenging, I first uploaded the images to an AWS S3 bucket, and then wrote a python script to pull the files. I used the `boto3` library to create an S3 client and used its `download_file` function to download the images individually and stored them in separate folders.

![Data Ingestion pipeline](image.png)

## Model Architecture
I employed **Transfer Learning** technique in this project by using the weights of the pre-trained **VGG-16** model. I then added a Global Max Pooling Layer to flatten the outputs of the VGG model. On top of that, I added a few more dense layers to get the final model, which has **14,888,380** non-trainable parameters and **173,692** trainable ones. I also used a dropout layer to avoid overfitting.

![Model Architecture](image1.png)

## Model Training & Experiment Tracking
**MLFlow** is an open-source library that allows developers to conduct experiments with their model. I used different sets of optimizer - **adam**, **sgd**, and **rmsprop**. I also tried different batch sizes (16, 32, and 64). I connected **MLFlow** with **DagsHub** which provides a repository to store the experiement results, thereby facilitating collaboration. Different developers working on the same project can try out different parameters, and the results would be accessible to each group member. **MLFlow** has the option to visualize the different metrics based on the parameters, which makes comparison all the more easier.

**MLFlow** also provides model versioning and the option to directly load and use the model just by adding a couple of lines of code.

The model with batch size **64** and optimizer **adam** gave the best performance among all the different settings. I was able to achieve the following metrics (average of all 4 classes) on the test dataset:

* Accuracy: **0.982**
* Precision: **0.981**
* Recall: **0.972**
* F1 score: **0.976**


![DagsHub UI](image-1.png)
![Batch Size Comparison](image-2.png)

### Confusion Matrix
![Confusion Matrix](confusion_matrix.png)

### Model Predictions
![Model Prediction](predictions.png)