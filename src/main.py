from PIL import Image
from fastapi import FastAPI, Depends, File, Form, UploadFile, HTTPException
from tensorflow import keras
import io
import numpy as np
import config
from error import ModelNotAvailableError
import database
import json

class Analyzer:
    def __init__(self) -> None:
        self.models: dict = {}

    def load_all_models(self):
        # loop through all the models setup in config
        for model in config.MODELS:
            new_model = PredictionModel()
            new_model.load_model(config.MODELS[model])
            new_model.labels = config.LABELS[model]
            self.models[model] = new_model

    
class PredictionModel:
    def __init__(self):
        self.model = None
        self.labels = None

    def load_model(self, path_to_model: str):
        self.model = keras.models.load_model(path_to_model)
        print(f"Succsefully loaded model from {path_to_model}")
        
    def predict(self, data):
        if not self.model:
            raise ModelNotAvailableError
        return self.model.predict(data)
    
    
app = FastAPI()

analyzer = Analyzer()
analyzer.load_all_models()
def get_analyzer():
    return analyzer

db = database.Database()
def get_db():
    return db

@app.get("/")
async def root():
    return {"message": "Server health page - running"}


@app.post("/api/v1/uploadfile")
async def create_upload_file(analyzer: Analyzer = Depends(get_analyzer), image: UploadFile = File(...), plant: str = Form(...)):
    if plant not in analyzer.models.keys():
        raise HTTPException(status_code=400, detail="There is no model available for the provided plant")
    
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    img = img.resize((256, 256))

    # Convert image to numpy array
    np_array = np.array(img)
    pred_model = analyzer.models[plant]

    # normalize the values
    #np_array = np_array / 255.0
    
    # add extra dimension for batch size
    input_batch = np.expand_dims(np_array, axis=0) 

    predictions = pred_model.predict(input_batch)

    api_data = {pred_model.labels[i]: float(predictions[0][i]) for i in range(len(pred_model.labels))}
    return api_data


@app.post("/api/v1/disease_detail")
async def disease_detail(disease_name: str = Form(...), plant_name: str = Form(...), database: database.Database = Depends(get_db)):
    disease_summary = db.query_disease_detail_specify_plant(disease_name=disease_name, plant_name=plant_name)
    if not disease_summary:
        pass #TODO return error response here
        print("query returned None")
        return
    return disease_summary

if __name__ == "__main__":
    import uvicorn
    #analyzer = Analyzer()
    #analyzer.load_all_models()
    uvicorn.run(app, host="localhost", port=8000)
