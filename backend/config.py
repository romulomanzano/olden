from dotenv import load_dotenv, find_dotenv
import os

# Import variables
load_dotenv(find_dotenv())

DATABASE_NAME = "olden"
API_ENDPOINT = "localhost:5000"
DATABASE_CONNECTION_STRING = os.getenv(
    "DATABASE_CONNECTION_STRING", "mongodb://localhost/{}".format(DATABASE_NAME)
)
COURIER_API_TOKEN = os.getenv("COURIER_API_TOKEN")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
FLASK_SALT = os.getenv("FLASK_SALT")
