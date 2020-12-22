from dotenv import load_dotenv, find_dotenv
import os

# Import variables
load_dotenv(find_dotenv())

MODE = os.getenv("MODE")
if MODE is None:
    raise ValueError("MODE can't be None")
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
if MODE == "production":
    TEST = False
    print("RUNNING IN PRODUCTION MODE")
else:
    TEST = True
    print("RUNNING IN DEVELOPMENT MODE")

# only allow calls originating from localhost 8080. this will change later
if TEST:
    WEB_ONLY_CORS_ORIGINS = ["http://localhost:8080", "http://localhost:5000"]
    API_CORS_ORIGINS = ["http://localhost:8080", "http://localhost:5000"]
else:
    WEB_ONLY_CORS_ORIGINS = [
        "https://web.olden.ai",
    ]
    API_CORS_ORIGINS = ["*"]
DAILY_API_URL = "https://api.daily.co/"
DAILY_API_KEY = os.getenv("DAILY_API_KEY")
MEETING_DEFAULT_LANGUAGE = (
    "en"  # see https://docs.daily.co/reference#room-configuration
)
MEETING_ROOM_DEFAULT_PREFIX = ""
COURIER_API_TOKEN = os.getenv("COURIER_API_TOKEN")
