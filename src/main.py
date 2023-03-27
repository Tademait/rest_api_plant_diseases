from PIL import Image
from fastapi import FastAPI, Depends, File, Form, UploadFile, HTTPException
from tensorflow import keras
import io
import numpy as np
import config
from error import ModelNotAvailableError
import database


class Analyzer:
    def __init__(self):
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
        print(f"Succesefully loaded model from {path_to_model}")
        
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

@app.get("/test_db")
async def test_db(db: database.Database = Depends(get_db)):
    plants = db.query_all_plants()
    if not plants:
        raise HTTPException(status_code=404, detail="No disease available in database")
    return [{f"plant": plant.name} for plant in plants]


@app.post("/api/v1/uploadfile")
async def create_upload_file(analyzer: Analyzer = Depends(get_analyzer), image1: UploadFile = File(...), image2: UploadFile = File(...), plant: str = Form(...)):
    if plant not in analyzer.models.keys():
        raise HTTPException(status_code=404, detail="No model available for the provided plant")
    
    contents = await image1.read()
    img = Image.open(io.BytesIO(contents))
    img = img.resize((256, 256))

    # Convert image to numpy array
    np_array = np.array(img)
    pred_model = analyzer.models[plant]

    # normalize the values
    np_array = np_array / 255.0
    
    # add extra dimension for batch size
    input_batch = np.expand_dims(np_array, axis=0) 

    predictions = pred_model.predict(input_batch)
    predictions = [{"name": pred_model.labels[i], "percentage": float(predictions[0][i])} for i in range(len(pred_model.labels))]
    predictions.sort(key=lambda x: x["percentage"], reverse=True)
    top_predictions = predictions[:5]
    return top_predictions


@app.post("/api/v1/disease_detail")
async def disease_detail(disease_name: str = Form(...), plant_name: str = Form(...), database: database.Database = Depends(get_db)):
    disease_summary = db.query_disease_detail_specify_plant(disease_name=disease_name, plant_name=plant_name)
    if not disease_summary:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease_summary


@app.post("/api/v1/disease_list")
async def disease_list(plant_name: str = Form(...), database: database.Database = Depends(get_db)):
    disease_list = db.query_all_diseases_for_plant(plant_name=plant_name)
    if not disease_list:
        return
    return disease_list

@app.get("/api/v1/plant_list")
async def plant_list():
    plant_list = db.query_all_plants()
    if not plant_list:
        raise HTTPException(status_code=404, detail="No plants found")
    return plant_list

@app.get("/api/v1/news_list")
async def news_list():
    news_list = db.query_all_news()
    if not news_list:
        raise HTTPException(status_code=404, detail="No news found")
    return news_list


if __name__ == "__main__":
    import uvicorn
    #analyzer = Analyzer()
    #analyzer.load_all_models()
    uvicorn.run(app, host="localhost", port=8000)
