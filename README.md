# README file for the Plant Disease Detection API

A simple REST API that receives get requests to analyze plant disease images
and returns the disease names and the confidence level of the prediction.

plan:
    + iterate through all the model files / folders and import each one of them as an object
    with its plant name that can then be used as key when sending the API request
    + create a function that receives the image and returns the prediction
    + create some basic authentication for the API (based on probably a secret token/key))
    + endpoints should be /api/v1/... <- specify the used model as either an id or a GET / POST parameter

pozn.:
+ data augmentation layer probably implicitly gets ignored when using the model.predict() function
  so it is used only when training the model -> no need to apply the augmentation via the lambdas
  on the dataset before
> Note that image data augmentation layers are only active during training (similarly to the Dropout layer).
(https://keras.io/guides/preprocessing_layers/)
+ add early stopping to the training process
+ decide between .h5 and .tf format for the model
+ add transfer learning to the model and choose a proper base model architecture


# Setup:

+ Preferably use a Python venv environment (https://docs.python.org/3/library/venv.html)
+ Install required libraries:

```
pip install -r requirements.txt
```

# Run:

> `uvicorn main:app --app-dir=src`

For a specific port, use the --port <port_number> flag.