# Analyzing Peripheral Blood Smear (PBS) images to detect Acute Lymphoblastic Leukemia
## Introduction
Acute lymphoblastic leukemia (ALL) is a type of cancer that affects the blood and bone marrow. It is characterized by the overproduction of immature white blood cells called lymphoblasts. ALL is the most common childhood cancer. It occurs when a bone marrow cell develops errors in its DNA.

This project analyzes **Peripheral Blood Smear** (PBS) images to to detect and classify 4 stages of **Acute Lymphoblastic Leukemia** - **Benign (Normal Stage)**, **Malignant Early**, **Malignant Pre**, and **Malignant Pro** stages.

The dataset we used was put together by a group of researchers, and I'm thankful for their work. It has around 3,000 PBS images, divided into four categories. The dataset is neatly organized, with separate folders for each category, and the images have easy-to-understand names.

Link to the research paper: https://onlinelibrary.wiley.com/doi/10.1002/int.22753

Link to the dataset: https://www.kaggle.com/datasets/mehradaria/leukemia


## Data Ingestion
To make the project a bit more challenging, I first uploaded the images to an AWS S3 bucket, and then wrote a python script to pull the files. I used the `boto3` library to create an S3 client and used its `download_file` function to download the images individually and stored them in separate folders.

![Screenshot 2023-10-25 121330](https://github.com/mohd-arham-islam/Blood-Cancer-Detection/assets/111959286/9a6b6686-c629-4e60-affe-c3efe0784100)


## Model Architecture
I employed **Transfer Learning** technique in this project by using the weights of the pre-trained **VGG-16** model. I then added a Global Max Pooling Layer to flatten the outputs of the VGG model. On top of that, I added a few more dense layers to get the final model, which has **14,888,380** non-trainable parameters and **173,692** trainable ones. I also used a dropout layer to avoid overfitting.

![image1](https://github.com/mohd-arham-islam/Blood-Cancer-Detection/assets/111959286/8b4be610-1476-49e0-9233-8f329df6f030)


## Model Training & Experiment Tracking
**MLFlow** is an open-source library that allows developers to conduct experiments with their model. I used different sets of optimizer - **adam**, **sgd**, and **rmsprop**. I also tried different batch sizes (16, 32, and 64). I connected **MLFlow** with **DagsHub** which provides a repository to store the experiement results, thereby facilitating collaboration. Different developers working on the same project can try out different parameters, and the results would be accessible to each group member. **MLFlow** has the option to visualize the different metrics based on the parameters, which makes comparison all the more easier.

**MLFlow** also provides model versioning and the option to directly load and use the model just by adding a couple of lines of code.

### DagsHub UI
![image-1](https://github.com/mohd-arham-islam/Blood-Cancer-Detection/assets/111959286/4690b29a-0051-46ab-b89c-998693468f0a)

### Comparing different parameters
![image-2](https://github.com/mohd-arham-islam/Blood-Cancer-Detection/assets/111959286/df9c1226-daf8-4b06-9afb-55e268ef7866)

## Model Metrics
The model with batch size **64** and optimizer **adam** gave the best performance among all the different settings. I was able to achieve the following metrics (average of all 4 classes) on the test dataset:

* Accuracy: **0.982**
* Precision: **0.981**
* Recall: **0.972**
* F1 score: **0.976**

### Confusion Matrix
![confusion_matrix](https://github.com/mohd-arham-islam/Blood-Cancer-Detection/assets/111959286/1058fdc5-b7ff-4987-9d1c-e0f193833af6)


### Model Predictions
![predictions](https://github.com/mohd-arham-islam/Blood-Cancer-Detection/assets/111959286/c68cb12c-7685-4d89-b10d-ffd8358ec013)


## Streamlit App
Instead of using an HTML+CSS Frontend, I used a simple Streamlit application to serve the model. The app asks the user to upload a PBS image, and when the "Predict" button is clicked, it gives the predicted class name along with the confidence level. Following is a screenshot of the app.

![Screenshot 2023-10-24 190828](https://github.com/mohd-arham-islam/Blood-Cancer-Detection/assets/111959286/63d88e3f-6ffc-48f3-b19b-52b97a37332c)


## Flask App
I also created a flask app to serve the model as an API. Upon getting an image file as an input, the API returns the class name and the confidence level. I will integrate this API with the frontend in the future.
Following is a screenshot of the API request sent using Postman.

![Screenshot 2023-10-24 165935](https://github.com/mohd-arham-islam/Blood-Cancer-Detection/assets/111959286/fd698b31-8ea9-41a7-a50b-9015b3afae50)


## Model Deployment
I deployed the application using an **AWS ECR** and an **AWS EC2** instance within a **CI/CD** pipeline, following these key steps:

* **Dockerfile Creation:** I started by creating a **Dockerfile** for the application, which defines how the application should be packaged and executed within a container.

* **ECR Repository:** Next, I established an **Amazon Web Services Elastic Container Registry** (ECR) repository to store the Docker images of the application.

* **EC2 Instance Configuration:** To support the application, I configured an **EC2** instance with 8GB of RAM, ensuring it meets the necessary resource requirements.

* **GitHub Self-Hosted Runner:** To automate the deployment process, I set up a **GitHub Self-Hosted Runner** on the EC2 instance, establishing a direct connection between the instance and the GitHub repository.

* **Continuous Integration:** Any new commits trigger the **CI/CD** pipeline. During the **Continuous Integration** phase, the latest code is pulled from the repository, ensuring it's readily available for subsequent stages.

* **Continuous Delivery:** In the **Continuous Delivery** phase, the Docker image is built and pushed to the ECR repository, making it accessible for deployment.

* **Continuous Deployment:** Finally, in the **Continuous Deployment** phase, the latest image is pulled from the ECR repository and executed to serve the application.

This streamlined pipeline ensures that any code changes are automatically built and deployed, facilitating a reliable and efficient deployment process.

### CI/CD Pipeline
![image](https://github.com/mohd-arham-islam/Blood-Cancer-Detection/assets/111959286/b9a47022-a200-4235-a0f7-bd1b8a87e8d8)


## Conclusion
In this project, I've harnessed advanced machine learning techniques to develop a robust Acute Lymphoblastic Leukemia (ALL) detection model. Leveraging Transfer Learning and extensive experimentation with MLflow, the model demonstrates exceptional accuracy. User-friendly interfaces, including a Streamlit application and a Flask API, enhance accessibility, while a well-structured deployment pipeline via AWS ECR and EC2 ensures efficient and reliable model deployment. This project's focus on healthcare applications underlines its commitment to advancing medical science and patient care.