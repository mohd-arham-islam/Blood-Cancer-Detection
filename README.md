# Analyzing Peripheral Blood Smear (PBS) images to detect Acute Lymphoblastic Leukemia
## Introduction
Acute lymphoblastic leukemia (ALL) is a type of cancer that affects the blood and bone marrow. It is characterized by the overproduction of immature white blood cells called lymphoblasts. ALL is the most common childhood cancer. It occurs when a bone marrow cell develops errors in its DNA.

This project analyzes **Peripheral Blood Smear** (PBS) images to to detect and classify 4 stages of **Acute Lymphoblastic Leukemia** - **Benign (Normal Stage)**, **Malignant Early**, **Malignant Pre**, and **Malignant Pro** stages.

The dataset we used was put together by a group of researchers, and I'm thankful for their work. It has around 3,000 PBS images, divided into four categories. The dataset is neatly organized, with separate folders for each category, and the images have easy-to-understand names.

Link to the research paper: https://onlinelibrary.wiley.com/doi/10.1002/int.22753

Link to the dataset: https://www.kaggle.com/datasets/mehradaria/leukemia

I employed Transfer Learning technique in this project by using the weights of the pre-trained **VGG-16** model. On top of that, I added a few more dense layers to get the final model, which has **14,888,380** non-trainable parameters and **173,692** trainable ones.

I was able to achieve the following metrics (average of all 4 classes) on the test dataset:

* Accuracy: **0.982**
* Precision: **0.981**
* Recall: **0.972**
* F1 score: **0.976**