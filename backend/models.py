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
    organizations = db.ListField(db.ReferenceField("Organization"))
    default_organization = db.ReferenceField("Organization")

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
        user_organization = Organization(name=user.email)
        user_organization.save()
        user.default_organization = user_organization
        user.organizations.append(user_organization)
        user.save()
        return user


class Member(db.DynamicDocument, HelperMixin):
    first_name = db.StringField()
    last_name = db.StringField()
    phone_number = db.StringField()
    email = db.StringField(max_length=255)
    organization = db.ReferenceField("Organization", required=True)
    active = db.BooleanField(default=True)
    archived = db.BooleanField(default=False)
    archived_date = db.DateTimeField()

    def mark_archived(self):
        self.archived = True
        self.active = False
        self.archived_date = datetime.datetime.utcnow()
        self.save()


class Organization(db.DynamicDocument, HelperMixin):
    name = db.StringField()


class VirtualEvent(db.DynamicDocument, HelperMixin):
    """
    This specifies a safety plan which is a relationship between
    users, devices, and alert settings.

    For simplicity we'll enforce a uniqueness on phone_number for ACTIVE contacts
    at the user level, however, we will allow a number to be re-entered in contact
    list if archived.
    """

    name = db.StringField()
    date = db.DateTimeField()
    organization = db.ReferenceField("Organization", required=True)
    original_timezone_name = db.StringField()
    estimated_duration_minutes = db.IntField()
    attendees = db.ListField(db.ReferenceField("Member"))
    created_by = db.ReferenceField("User")
    created_date = db.DateTimeField()
    created_under_timezone = db.StringField()
    canceled = db.BooleanField(default=False)
    canceled_date = db.DateTimeField()
    canceled_by = db.ReferenceField("User")
    alert_settings = db.ReferenceField("AlertSettings")

    @staticmethod
    def get_organization_events(organization):
        events = VirtualEvent.objects(canceled__ne=True, organization=organization)
        return events

    @staticmethod
    def create(**kwargs):
        event = VirtualEvent(**kwargs)
        event.save()
        settings = AlertSettings(virtual_event=event)
        settings.save()
        event.alert_settings = settings
        event.save()
        return event

    def cancel(self, user):
        self.canceled = True
        self.canceled_date = datetime.datetime.utcnow()
        self.canceled_by = user
        self.save()

    def add_attendee(self, attendee):
        self.attendees.append(attendee)
        self.save()

    def remove_attendee(self, attendee):
        self.attendees.remove(attendee)
        self.save()


class AlertSettings(db.DynamicDocument, HelperMixin):
    """
    This specifies the alert settings for a given safety plan
    """

    virtual_event = db.ReferenceField("VirtualEvent")
    sms = db.BooleanField(default=True)
    email = db.BooleanField(default=True)
    prerecorded_voice = db.BooleanField(default=False)
