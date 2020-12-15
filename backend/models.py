"""Module where all the MongoDb definitions go"""

from flask import Flask
import logging
from flask_mongoengine import MongoEngine
import config
import utils
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import datetime
from mongoengine.queryset.visitor import Q
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.config["MONGODB_DB"] = config.DATABASE_NAME
app.secret_key = config.FLASK_SECRET_KEY
app.config["SECURITY_PASSWORD_SALT"] = config.FLASK_SALT
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.JWT_REFRESH_TOKEN_EXPIRES
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config["JWT_HEADER_TYPE"] = config.JWT_HEADER_TYPE
app.config["JWT_HEADER_NAME"] = config.JWT_HEADER_NAME

app.config["MONGODB_SETTINGS"] = {
    "host": config.DATABASE_CONNECTION_STRING,
    "tz_aware": False,
    "connect": False,
}

jwt = JWTManager(app)
db = MongoEngine(app)
flask_bcrypt = Bcrypt(app)
CORS(app)


class HelperMixin:
    pass


class BlacklistedToken(db.DynamicDocument):
    jti = db.StringField()
    revoked = db.BooleanField()


@utils.logged
class User(db.DynamicDocument, HelperMixin):
    """Represents a generic user of web app"""

    email = db.StringField(max_length=255)
    password = db.BinaryField()
    first_name = db.StringField()
    last_name = db.StringField()
    registered_date = db.DateTimeField()

    def create_access_token(self):
        """Generate access token based on what's considered unique identifier"""
        return create_access_token(identity=dict(id=str(self.id)))

    @staticmethod
    def create_find_user(email):
        """
        if existing user, return it, otherwise, create unregistered
        """
        user = User.objects(email=email).first()
        if user:
            return user
        user = User(
            email=email,
            registered=datetime.datetime.utcnow(),
        )
        user.save()
        return user
