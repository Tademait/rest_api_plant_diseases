from dotenv import load_dotenv
import os

# load all the secret .env variables
load_dotenv()
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

# set the port on which the uvicorn server should be running
PORT = 8000

# points plant to according model
MODELS = {"tomato": "tomato_model/v1/", "grape": "grape_model/v1/"}

# proper labels for each model
_TOMATO_LABELS = ['bacterial spot', 'early blight', 'late blight',
                  'leaf mold', 'septoria leaf spot', 'spider mites',
                  'target spot', 'yellow leaf curl virus', 'mosaic virus', 'healthy']

_GRAPE_LABELS = ['black rot', 'esca', 'leaf blight', 'healthy']

LABELS = {"tomato": _TOMATO_LABELS, "grape": _GRAPE_LABELS}
# add any other model here in the same manner...

# image collection configuration
COLLECTION_ENABLED = True
COLLECTION_PATH = 'image_collection/'

# specify the default input size for models
IMG_DIMENSIONS = (256, 256)
