# This script will create the desired folder structure
import os
from pathlib import Path
import logging

# Setting up a logging string
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s:'
)

projectName = 'cnnClassifier'
fileList = [
    '.github/workflows/.gitkeep',  #.gitkeep is just to make sure the folder isn't empty
    f'src/__init__.py',
    f'src/components/__init__.py',
    f'src/utils/__init__.py',
    f'src/config/__init__.py',
    f'src/config/configuration.py',
    f'src/pipeline/__init__.py',
    f'src/entity/__init__.py',
    f'src/constants/__init__.py',
    'config/config.yaml',
    'dvc.yaml',
    'params.yaml',
    'requirements.txt',
    'setup.py',
    'research/trials.ipynb',
    'templates/index.html'
]

for file in fileList:
    filePath = Path(file)
    fileDir, fileName = os.path.split(filePath)

    # Code to make the folder
    if fileDir != '':
        os.makedirs(fileDir, exist_ok=True)
        logging.info(f'Creating directory {fileDir} for the file {fileName}')

    # Code to make the files
    if (not os.path.exists(filePath)) or (os.path.getsize(filePath)==0):
        with open(filePath, 'w') as f:
            pass
            logging.info(f'Creating empty file {filePath}')
    
    else:
        logging.info(f'{fileName} already exists')