# README file for the Plant Disease Identification API

A REST API and a plant disease identification app backend that handles database queries, 
requests to analyze plant disease images and which returns the disease names and the
confidence level of the prediction.

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

## Install Python
Depending on your distribution, install python 3 and pip. For example, on Ubuntu:

```
sudo apt install python3 python3-pip
```
You can also install python from the official website: https://www.python.org/downloads/
The application is tested and live version is running on Python 3.10.7

## Setup virtual environment
+ Preferably use a Python venv environment (https://docs.python.org/3/library/venv.html)
> Note: you can skip this step, although it is recommended for managing your python dependencies.

```
python -m venv myenv_name
```

To activate the venv on Windows, run:
  
```
myenv_name\Scripts\activate.bat
```
For Linux/macOS:

```
source myenv_name/bin/activate
```
To later deactivate the venv, run:

```
deactivate
```

With your venv activated, you can now install the required libraries.


## Install required libraries

```
pip install -r src/requirements.txt
```

## Setup database and .env file
+ You need to create a new PostgreSQL database (recommended version 15):
https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart

You also need to create a .env file inside the `src/` directory for a secret connection string. Set the
database connection string in the .env file as the following example, replacing the respective values with your own:

```
DB_CONNECTION_STRING="postgresql://username:password@domain:port/db_name"
```


# Run:

> `uvicorn main:app --app-dir=src`

For a specific port, use the --port <port_number> flag.

# Testing
To run the tests, run the following command root directory of the project:

```
pytest
```
> Note: make sure you have the pytest library installed: `pip install pytest`


# Project overview
You can find all the available endpoints on the /docs page.
For example, if you are running the server on localhost, you can access the docs page at http://localhost:8000/docs

The main structure of the project is as follows:

the `src` directory contains the trained tensorflow models. The models are loaded in the `main.py` file,
which is the entry point of the application. They are loaded based on the paths provided in `config.py`.
The `main.py` file contains the FastAPI endpoints and handling of the incoming requests. The database
communication and ORM classes are handled inside the `database.py` file. 

Currently, a live version of the application is hosted at `render.com` with database being hosted on
a dedicated VPS at `digitalocean.com`. The live REST API can be accessed at https://plant-rest-api.onrender.com (note that it might take several minutes to spin-up the sleeping container).

# Credits
App is developed under the [Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/legalcode) license.

Plant information, treatment and example disease images are sourced from the [PlantVillage website](https://plantvillage.psu.edu)
