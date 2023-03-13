class ModelNotAvailableError(Exception):
    def __init__(self, error_code=950):
        self.message = "Unable to access model of the PredictionModel class"
        self.error_code = error_code

    def __str__(self):
        return f"{self.message}"