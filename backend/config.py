from dotenv import load_dotenv, find_dotenv
import os

# Import variables
load_dotenv(find_dotenv())

DATABASE_NAME = "olden"
LOG_LEVEL = "INFO"
API_ENDPOINT = "localhost:5000"
DATABASE_CONNECTION_STRING = os.getenv(
    "DATABASE_CONNECTION_STRING", "mongodb://localhost/{}".format(DATABASE_NAME)
)
COURIER_API_TOKEN = os.getenv("COURIER_API_TOKEN")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
FLASK_SALT = os.getenv("FLASK_SALT")
COTTER_JWKS_URL = "https://www.cotter.app/api/v0/token/jwks"
COTTER_API_KEY = os.getenv("COTTER_API_KEY")
COTTER_API_SECRET = os.getenv("COTTER_API_SECRET")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = 86400 * 1  # 1 day in seconds
JWT_REFRESH_TOKEN_EXPIRES = 86400 * 5  # 5 day in seconds
JWT_HEADER_TYPE = "Bearer"
JWT_HEADER_NAME = "Authorization"
