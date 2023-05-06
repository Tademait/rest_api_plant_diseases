# README file for the Plant Disease Identification API

Author: Tadeas Kozub
Mail: xkozub06@vutbr.cz
Year: 2022/2023

A REST API and a plant disease identification app backend that handles database queries, 
requests to analyze plant disease images and which returns the disease names and the
confidence level of the prediction.


# Setup:

## Install Python
Depending on your distribution, install python 3 and pip. For example, on Ubuntu:

```
sudo apt install python3 python3-pip
```
You can also install python from the official website: https://www.python.org/downloads/
> Note: The application is tested and live version is running on Python 3.10.7

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
To run the tests, run the following command in the root directory of the project:

```
pytest
```
> Note: make sure you have the pytest library installed: `pip install pytest`


# Project overview
You can find all the available endpoints on the `/docs` page.
For example, if you are running the server on localhost, you can access the docs page at http://localhost:8000/docs

The main structure of the project is as follows:

the `src` directory contains the main source code of the app. The models are loaded in the `main.py` file,
which is the entry point of the application. They are loaded based on the paths provided in `config.py`.
The `main.py` file contains the FastAPI endpoints and handling of the incoming requests. The database
communication and ORM classes are handled inside the `database.py` file. The actual loading of modules is
handled by the *Analyzer* class in the `analyzer.py` file. 

Currently, a live version of the application is hosted at `tkozub.me` with database being hosted on
a dedicated VPS at `digitalocean.com`. The live REST API can be accessed at https://tkozub.me/api/v1.
In case there is an issue with the live version, you can run the application locally by following the
instructions above or you can contact me at `xkozub06@vutbr.cz`.

> Note: Secure connection to the server is provided via Nginx and Let's Encrypt. SSL certs are generated using the tool Certbot.

# Credits

Plant information, treatment and example disease images are sourced from the [PlantVillage website](https://plantvillage.psu.edu)
