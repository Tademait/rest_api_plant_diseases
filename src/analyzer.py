import config
from error import ModelNotAvailableError
from tensorflow import keras

class Analyzer:
    def __init__(self):
        """
        Initializes the dictionary
        that will hold all the model objects
        """
        self.models: dict = {}

    def load_all_models(self):
        """
        Loops through all the models setup in config
        and their label to populate the dictionary
        """
        for model in config.MODELS:
            new_model = PredictionModel()
            new_model.load_model(config.MODELS[model])
            new_model.labels = config.LABELS[model]
            self.models[model] = new_model

    
class PredictionModel:
    def __init__(self):
        """
        Initializes the model object
        """
        self.model = None
        self.labels = None

    def load_model(self, path_to_model: str):
        """
        Loads the trained and saved model into memory

        Args:
            path_to_model (str): path to where the model is stored
            the model should be either in .h5 or preferably in the
            tensorflow folder format
        """
        self.model = keras.models.load_model(path_to_model)
        print(f"Succesefully loaded model from {path_to_model}")
        
    def predict(self, data):
        """ 
        Calls the predict method of a specific model based
        on selected plant

        Args:
            data (numpy array)

        Raises:
            ModelNotAvailableError: if no model is found for 
            the given plant, raise an error

        Returns:
            vector of predictions with applied softmax func
        """
        if not self.model:
            raise ModelNotAvailableError
        return self.model.predict(data)