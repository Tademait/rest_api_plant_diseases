from PIL import Image
from fastapi import FastAPI, Depends, File, Form, UploadFile
from tensorflow import keras
from pydantic import BaseModel
import io
import numpy as np
import json

class Analyzer:
    def __init__(self) -> None:
        # self.model_dict = {}
        pass 
    
    def load_all_models(self):
        # loop through either all the folders or load from config
        # for model in models_dir:
        #   dict[mode_name] = PredictionModel()
        #   dict[mode_name].load_model() # maybe load as part of initializer
        pass
        
    
class PredictionModel:
    def __init__(self):
        self.model = None

    def load_model(self, path_to_model: str):
        self.model = keras.models.load_model(path_to_model)
        print(f"Succsefully loaded model from {path_to_model}")
        #print(self.model.summary())

    @staticmethod
    def prepare_data(data):
        # check the sent data is a valid image (preferably square, but should crop while keeping aspect ratio anyways)
        # normalize the data
        prepared_data = data
        return prepared_data
        
        
    def predict(self, data):
        if not self.model:
            raise NotImplementedError #todo implement own Error class
        # prepared_data = self.prepare_data()
        return self.model.predict(data)
    
    
app = FastAPI()
def prepare_analyzer():
    return Analyzer()

@app.get("/")
async def root(analyzer_obj: Analyzer = Depends(prepare_analyzer)):
    analyzer_obj.load_all_models()
    return {"message": "Hello World"}


@app.post("/api/v1/uploadfile")
async def create_upload_file(image: UploadFile = File(...), plant: str = Form(...)):
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    img = img.resize((256, 256))
    
    # Convert image to numpy array
    np_array = np.array(img)
    print(np.info(np_array))
    tomato_model = PredictionModel()
    tomato_model.load_model("tomato_model/v1/")
    
    np_array = np_array / 255.0
    # add extra dimension for batch size
    input_batch = np.expand_dims(np_array, axis=0) 
    
    predictions = tomato_model.predict(input_batch)
    np.set_printoptions(formatter={'float_kind':'{:f}'.format})
    print(predictions)
    
    #! todo: make this more generic, either save the labels as part of model, or inside the folder
    class_labels = ['tomato_bacterial_spot', 'tomato_early_blight', 'tomato_late_blight',
                    'tomato_leaf_mold', 'tomato_septoria_leaf_spot', 'tomato_spider_mites',
                    'tomato_target_spot', 'tomato_yellow_leaf_curl_virus', 'tomato_mosaic_virus', 'tomato_healthy']


    api_data = {class_labels[i]: float(predictions[0][i]) for i in range(len(class_labels))}
    return api_data
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
    # tomato_model = PredictionModel()
    # tomato_model.load_model("tomato_model/v1/")
    # plant_models = {"tomato": tomato_model}
    #analyzer_obj = prepare_analyzer()
    
    # when calling the identify endpoint:
    # + on startup, load-up every plant model - either based on loop through
    # model folders or load-up from manually setupped config
    # + check the dict, if model is loaded
    # + if not, throw error
    # + identify