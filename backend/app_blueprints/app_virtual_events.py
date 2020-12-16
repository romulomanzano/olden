""""Module to house the emergency related endpoints"""
import config as config
from flask import Blueprint, request
from models import VirtualEvent, User
from flask_jwt_extended import jwt_required
from flask_cors import CORS
from .app_utils import get_user_for_token_identity
from utils import get_generic_logger
from bson.json_util import dumps
from bson import ObjectId
import bson
import mongoengine
from mongoengine.queryset.visitor import Q
from api_schemas.virtual_event_schemas import event_list_schema
import cerberus

# define the blueprint variable
app_events_blueprint = Blueprint("app_virtual_events", __name__)
# allow for cross site origins
cors = CORS(app_events_blueprint, origins=config.API_CORS_ORIGINS)
logger = get_generic_logger(__name__)


@app_events_blueprint.route("/user/virtual_events", methods=["GET"])
@jwt_required
def get_user_virtual_events():
    user = get_user_for_token_identity()
    if user:
        # specific mongo query
        events = VirtualEvent.get_all_user_events(user)
        normalizer = cerberus.Validator(event_list_schema, purge_unknown=True)
        event_list = normalizer.normalized(
            {"events": [x.to_mongo().to_dict() for x in events]}
        )
        return (dumps(event_list), 200)
    return dumps({"ok": False, "message": "Invalid user"}), 400
