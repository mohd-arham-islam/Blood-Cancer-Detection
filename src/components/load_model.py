from dotenv import load_dotenv
import mlflow
from src.utils import saveObject

load_dotenv()

logged_model = 'runs:/4dad99af7e0f4e16b3813e880fe511d5/cnn'
model = mlflow.pyfunc.load_model(logged_model)

saveObject(
    filePath='artifacts/MLFlow_model.pkl',
    object=model
)