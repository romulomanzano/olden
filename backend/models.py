"""Module where all the MongoDb definitions go"""

from flask import Flask
import logging
from flask_mongoengine import MongoEngine
import config
import utils
from flask_bcrypt import Bcrypt
import constants as CONSTANTS
import datetime
from communications import (
    Notifier,
    VERIFY_ACCOUNT_PHONE_NUMBER,
    VERIFY_CAREGIVER_PHONE_NUMBER,
    RESET_PASSWORD,
)
from mongoengine.queryset.visitor import Q

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.config["MONGODB_DB"] = config.DATABASE_NAME
app.secret_key = config.FLASK_SECRET_KEY
app.config["SECURITY_PASSWORD_SALT"] = config.FLASK_SALT
app.config["MONGODB_SETTINGS"] = {
    "host": config.DATABASE_CONNECTION_STRING,
    "tz_aware": False,
    "connect": False,
}

db = MongoEngine(app)
flask_bcrypt = Bcrypt(app)


@utils.logged
class User(db.DynamicDocument, HelperMixin):
    """Represents a generic user of web app"""

    email = db.StringField(max_length=255)
    password = db.BinaryField()
    first_name = db.StringField()
    last_name = db.StringField()
    registered = db.BooleanField(default=False)
    registered_date = db.DateTimeField()
