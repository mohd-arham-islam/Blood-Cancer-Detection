import os
import sys
import logging

# ------------ Custom Exception -----------------------
def errorMessageDetail(error, errorDetail:sys):
    _, _, exc_tb = errorDetail.exc_info()
    fileName = exc_tb.tb_frame.f_code.co_filename
    lineNumber = exc_tb.tb_lineno
    errorMessage = f'''Error occured in python file {fileName}, 
    line number {lineNumber}. Error Message: {str(error)}    
    '''

    return errorMessage

class customException(Exception):
    def __init__(self, errorMessage, errorDetail:sys):
        super().__init__(errorMessage)
        self.errorMessage = errorMessageDetail(errorMessage, errorDetail)

    def __str__(self):
        return self.errorMessage
    
# ------------ Logger Setup -------------------------------------------------------

loggingString = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
logDir = 'logs'
logFilePath = os.path.join(logDir, 'Logs.log')
os.makedirs(logDir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=loggingString,

    handlers=[
        logging.FileHandler(logFilePath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('Logger')