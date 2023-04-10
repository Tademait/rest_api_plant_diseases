from dotenv import load_dotenv
import os

# load all the secret .env variables
load_dotenv()
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

# points plant to according model
MODELS = {"tomato": "/var/data/tomato_model/v3/"}

# proper labels for each model
_TOMATO_LABELS = ['bacterial spot', 'early blight', 'late blight',
                  'leaf mold', 'septoria leaf spot', 'spider mites',
                  'target spot', 'yellow leaf curl virus', 'mosaic virus', 'healthy']

LABELS = {"tomato": _TOMATO_LABELS}

# image collection configuration
COLLECTION_ENABLED = True
COLLECTION_PATH = 'image_collection/'

# specify generic input size for models
IMG_DIMENSIONS = (256, 256)
