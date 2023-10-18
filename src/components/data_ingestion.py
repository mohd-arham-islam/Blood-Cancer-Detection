import os
import sys
from dataclasses import dataclass
from src import logger
from src import customException
from dotenv import load_dotenv
import boto3

# Reading the private access keys from .env file
load_dotenv()

@dataclass()
class DataIngestionConfig:
    # Defining the path of images
    benignImagesPath = os.path.join('artifacts', 'images', 'Benign')
    earlyImagesPath = os.path.join('artifacts', 'images', 'Early')
    preImagesPath = os.path.join('artifacts', 'images', 'Pre')
    ProImagesPath = os.path.join('artifacts', 'images', 'Pro')

    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    bucketName = 'bloodcancerimages'

class DataIngestion:
    def __init__(self):
        self.ingestionConfig = DataIngestionConfig()
    
    def initiateDataIngestion(self):
        logger.info('Initiating Data Ingestion')

        try:
            # Creating the image directories
            os.makedirs(self.ingestionConfig.benignImagesPath, exist_ok=True)
            os.makedirs(self.ingestionConfig.earlyImagesPath, exist_ok=True)
            os.makedirs(self.ingestionConfig.preImagesPath, exist_ok=True)
            os.makedirs(self.ingestionConfig.ProImagesPath, exist_ok=True)
            logger.info('Created the Image Directories')

            # Creating the AWS S3 client
            s3 = boto3.resource(
                service_name='s3',
                region_name='ap-south-1',
                aws_access_key_id=self.ingestionConfig.AWS_ACCESS_KEY,
                aws_secret_access_key=self.ingestionConfig.AWS_SECRET_ACCESS_KEY
            )
            logger.info('Created S3 Client')

            bucketName = self.ingestionConfig.bucketName
            images = list(s3.Bucket('bloodcancerimages').objects.all())
            logger.info(f'Successfully read {len(images)} images from the S3 bucket {bucketName}')

            for image in images:
                key = image.key
                
                dir = key.split('/')
                folder = dir[0]
                file = dir[1]

                downloadPath = os.path.join('artifacts', 'images', folder, file)
                s3.Bucket('bloodcancerimages').download_file(
                Key=key, 
                Filename=downloadPath
                )
            logger.info(f'Successfully downloaded {len(images)} from the S3 bucket {bucketName}')
            
        
        except Exception as e:
            raise customException(e, sys)

if __name__=="__main__":
    ingestionObject = DataIngestion()
    ingestionObject.initiateDataIngestion()