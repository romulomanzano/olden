"""Module where all the MongoDb definitions go"""

from flask import Flask
import logging
from flask_mongoengine import MongoEngine
import config
import utils
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import datetime
import constants
from communications.communications import Notifier
from flask_jwt_extended import create_access_token, JWTManager
from call_orchestrator import CallOrchestrator
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk

if config.SENTRY_DSN:
    if config.MODE == "production":
        traces_sample_rate = 0.10
    else:
        traces_sample_rate = 0
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=[FlaskIntegration()],
        environment=config.MODE,
        attach_stacktrace=True,
        send_default_pii=True,
        traces_sample_rate=traces_sample_rate,
    )

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


@utils.logged
class MeetingConfig(db.EmbeddedDocument):
    start_audio_off = db.BooleanField(
        default=False,
    )
    start_video_off = db.BooleanField(default=False)
    exp = db.DateTimeField()
    nbf = db.DateTimeField()
    max_participants = db.IntField()
    eject_after_elapsed = db.IntField()
    eject_at_room_exp = db.BooleanField()
    lang = db.StringField()


@utils.logged
class MeetingDetails(db.EmbeddedDocument):

    _id = db.StringField()
    name = db.StringField()
    api_created = db.BooleanField()
    privacy = db.StringField()
    url = db.StringField()
    created_at = db.DateTimeField()
    config = db.EmbeddedDocumentField(MeetingConfig)


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
    address = db.ReferenceField("Address")
    phone_number = db.StringField()

    @property
    def contact_profile(self):
        return {"phone_number": self.phone_number, "email": self.email}

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
        user_organization = Organization()
        user_organization.save()
        user_organization.create_instant_meeting_link()
        user.default_organization = user_organization
        user.organizations.append(user_organization)
        # notify user registered
        if not config.TEST:
            Notifier().notify_organizer("New user registered {}".format(user.email))
        user.save()

        return user

    def set_personal_details_from_web_data(self, data):
        self.first_name = data.get("firstName")
        self.last_name = data.get("lastName")
        self.save()
        if self.phone_number != data.get("phoneNumber"):
            self.phone_number = data.get("phoneNumber")
            self.save()

    def get_personal_details_dict(self):
        personal_details = {}
        personal_details["first_name"] = self.first_name
        personal_details["last_name"] = self.last_name
        personal_details["phone_number"] = self.phone_number
        return personal_details

    @property
    def _contact_profile(self):
        return {"phone_number": self.phone_number, "email": self.email}


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

    @property
    def contact_profile(self):
        return {"phone_number": self.phone_number, "email": self.email}


class Organization(db.DynamicDocument, HelperMixin):
    name = db.StringField()
    max_participants_per_meeting = db.IntField(default=20)
    permanent_meeting_details = db.EmbeddedDocumentField(MeetingDetails)

    def create_instant_meeting_link(self):
        orch = CallOrchestrator()
        details = orch.create_permanent_room()
        meeting_details = MeetingDetails(**details)
        self.permanent_meeting_details = meeting_details
        self.save()

    def get_upcoming_event_count(self, now=None):
        now = datetime.datetime.utcnow()
        events = VirtualEvent.objects(
            canceled__ne=True, organization=self, date__gte=now
        )
        return events.count()

    def get_past_event_count(self, now=None):
        now = datetime.datetime.utcnow()
        events = VirtualEvent.objects(
            canceled__ne=True, organization=self, date__lt=now
        )
        return events.count()

    def get_active_member_count(self, now=None):
        now = now or datetime.datetime.utcnow()
        members = Member.objects(active=True, organization=self)
        return members.count()

    def account_summary(self):
        return {
            "upcoming_events": self.get_upcoming_event_count(),
            "past_events": self.get_past_event_count(),
            "active_members": self.get_active_member_count(),
            "instantMeetingLink": self.permanent_meeting_details.url,
        }


@utils.logged
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
    meeting_details = db.EmbeddedDocumentField(MeetingDetails)
    reminders_sent = db.ListField(db.StringField(), default=[])

    def create_meeting_event(self):
        orch = CallOrchestrator()
        details = orch.create_room(
            start_datetime=self.date,
            duration_estimate_minutes=self.estimated_duration_minutes,
            eject_at_room_exp=True,
            max_participants=self.organization.max_participants_per_meeting,
        )
        meeting_details = MeetingDetails(**details)
        self.meeting_details = meeting_details
        self.save()

    @staticmethod
    def get_organization_events(organization, event_type=None):
        if not event_type:
            events = VirtualEvent.objects(canceled__ne=True, organization=organization)
        elif event_type == "past":
            now = datetime.datetime.utcnow()
            events = VirtualEvent.objects(
                canceled__ne=True, organization=organization, date__lt=now
            )
        elif event_type == "upcoming":
            now = datetime.datetime.utcnow()
            events = VirtualEvent.objects(
                canceled__ne=True, organization=organization, date__gte=now
            )
        return events

    @staticmethod
    def create(**kwargs):
        event = VirtualEvent(**kwargs)
        event.save()
        settings = AlertSettings(virtual_event=event)
        settings.save()
        event.alert_settings = settings
        event.save()
        event.create_meeting_event()
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


class Address(db.DynamicDocument, HelperMixin):
    """Generic address container"""

    date_updated = db.DateTimeField()
    address_line_1 = db.StringField()
    city = db.StringField()
    zipcode = db.StringField()
    state = db.StringField()
    land_line_number = db.StringField()
    country = db.StringField(default=constants.ADDRESS_UNITED_STATES)
    user = db.ReferenceField("User")

    def update_address_from_web_data(self, data, now=None):
        now = now or datetime.datetime.utcnow()
        self.address_line_1 = data.get("addressLine1")
        self.zipcode = data.get("zipCode")
        self.city = data.get("city")
        self.state = data.get("state")
        self.date_updated = now
        self.land_line_number = data.get("landLineNumber")
        self.save()

    @staticmethod
    def create_address_from_web_data(data, now=None):
        now = now or datetime.datetime.utcnow()
        address = Address()
        address.address_line_1 = data.get("addressLine1")
        address.zipcode = data.get("zipCode")
        address.city = data.get("city")
        address.state = data.get("state")
        address.date_updated = now
        address.land_line_number = data.get("landLineNumber")
        address.save()
        return address
