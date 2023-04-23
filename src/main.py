from analyzer import Analyzer
from datetime import datetime
from fastapi import FastAPI, Depends, File, Form, UploadFile, HTTPException
import io
import numpy as np
from PIL import Image
from tensorflow import keras

import config
import database

# create the FastAPI app object that will be run in the main function
app = FastAPI()

# create the analyzer object that handles loading and selection of proper model
analyzer = Analyzer()
analyzer.load_all_models()

# getter function to reuse the object using FastApi dependencies
def get_analyzer():
    return analyzer

# create a db object that manages all the DB connections and queries
db = database.Database()

# getter function to reuse the object using FastApi dependencies
def get_db():
    return db

# GET endpoint for root, only used to check if the server is up and running
@app.get("/")
async def root():
    return {"message": "Server health page - running"}

# GET endpoint to test the db connection alongisde REST API functionality
# from outside of the server
@app.get("/test_db")
async def test_db(db: database.Database = Depends(get_db)):
    plants = db.query_all_plants()
    if not plants:
        raise HTTPException(status_code=404, detail="No disease available in database")
    return plants

# POST endpoint to upload two images, analyze them using proper model and send answer with
# the most probable diseases and percentages
@app.post("/api/v1/uploadfile")
async def analyze_images(analyzer: Analyzer = Depends(get_analyzer),
                         image1: UploadFile = File(...), image2: UploadFile = File(...),
                         plant: str = Form(...)):
    if plant not in analyzer.models.keys():
        raise HTTPException(status_code=500, 
                            detail="No model available for the provided plant")
    
    # select proper model for the requested plant
    pred_model = analyzer.models[plant]
    
    # convert the images from binary data using PIL
    contents1 = await image1.read()
    img1 = Image.open(io.BytesIO(contents1))
    contents2 = await image2.read()
    img2 = Image.open(io.BytesIO(contents2))
    
    # collect the image to enlarge dataset
    if config.COLLECTION_ENABLED:
        try:
            file_name = datetime.now().strftime('%Y_%m_%d-%I_%M_%S')
            img1.save(f"{config.COLLECTION_PATH}/{file_name}-1.jpg")
            img2.save(f"{config.COLLECTION_PATH}/{file_name}-2.jpg")
        except:
            print("Failed to save images")

    # resize the image to input dimensions of the model
    img1 = img1.resize(config.IMG_DIMENSIONS)
    img2 = img2.resize(config.IMG_DIMENSIONS)
    
    # Convert images to RGB mode to remove the alpha channel if present
    # (for example in case the user sends a .PNG image)
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    
    # Convert image to numpy array
    np_array1 = np.array(img1)
    np_array2 = np.array(img2)

    # normalize the values
    keras.applications.xception.preprocess_input(np_array1)
    keras.applications.xception.preprocess_input(np_array2)
    
    # add extra dimension to create a batch of size 1
    input_batch1 = np.expand_dims(np_array1, axis=0)
    input_batch2 = np.expand_dims(np_array2, axis=0)

    # gather predictions from both models
    predictions1 = pred_model.predict(input_batch1)
    predictions2 = pred_model.predict(input_batch2)
    
    # concat the results and find max value for each pair
    predictions_concat = np.concatenate((predictions1.reshape(-1, 1), predictions2.reshape(-1, 1)), axis=1)
    predictions = np.amax(predictions_concat, axis=1)

    # adjust the weights of the predictions to add up to 1 (100%) again
    predictions = predictions / np.sum(predictions)

    # create a list of dictionaries with the results and return at most top 5 predictions
    predictions_array = [{"name": pred_model.labels[i], "percentage": float(predictions[i])} for i in range(len(pred_model.labels))]
    predictions_array.sort(key=lambda x: x["percentage"], reverse=True)
    top_predictions = predictions_array[:5]
    return top_predictions

# POST endpoint to get a detail info of disease
# based on disease name and plant name
@app.post("/api/v1/disease_detail")
async def disease_detail(disease_name: str = Form(...), plant_name: str = Form(...),
                         db: database.Database = Depends(get_db)):
    disease_summary = db.query_disease_detail_specify_plant(disease_name=disease_name, 
                                                            plant_name=plant_name)
    if not disease_summary:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease_summary

# POST endpoint to get a list of diseases
# for a concrete plant
@app.post("/api/v1/disease_list")
async def disease_list(plant_name: str = Form(...), db: database.Database = Depends(get_db)):
    disease_list = db.query_all_diseases_for_plant(plant_name=plant_name)
    if not disease_list:
        return
    return disease_list

# GET endpoint to get a list of
# currently supported plant names
@app.get("/api/v1/plant_list")
async def plant_list():
    plant_list = db.query_all_plants()
    if not plant_list:
        raise HTTPException(status_code=404, detail="No plants found")
    return plant_list

# GET endpoint to get a list of news
# regarding the operation of the server and app
@app.get("/api/v1/news_list")
async def news_list():
    news_list = db.query_all_news()
    if not news_list:
        raise HTTPException(status_code=404, detail="No news found")
    return news_list

# run the uvicorn server application on the selected port
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=config.PORT)
