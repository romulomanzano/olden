""""Module to house the auth related endpoints"""
import config as config
import constants as constants
from flask import Blueprint, request
from models import Address, User
from flask_jwt_extended import jwt_required
from flask_cors import CORS
from .app_utils import get_user_for_token_identity
from utils import get_generic_logger
from bson.json_util import dumps

# define the blueprint variable
app_profile_blueprint = Blueprint("app_profile", __name__)
# allow for cross site origins
cors = CORS(app_profile_blueprint, origins=config.WEB_ONLY_CORS_ORIGINS)
logger = get_generic_logger(__name__)


@app_profile_blueprint.route("/user/profile", methods=["GET"])
@jwt_required
def get_user_profile_data():
    """
    Get user data if available
    """
    user = get_user_for_token_identity()
    if user:
        # set address
        if user.address:
            address = user.address.to_mongo().to_dict()
        else:
            address = {}
        personal_details = user.get_personal_details_dict()
        return dumps({"personal_info": personal_details, "address": address}), 200
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_profile_blueprint.route("/user/profile", methods=["POST"])
@jwt_required
def user_profile_data():
    """
    Save user data
    """
    user = get_user_for_token_identity()
    if user:
        data = request.json
        if user.address:
            user.address.update_address_from_web_data(data.get("address"))
        else:
            address = Address.create_address_from_web_data(data.get("address"))
            user.address = address
            user.save()
        # personal details
        user.set_personal_details_from_web_data(data.get("personalInfo"))
        return (
            dumps(
                {
                    "profile": {
                        "personal_info": user.get_personal_details_dict(),
                        "address": user.address.to_mongo().to_dict(),
                    },
                    "message": "Profile updated successfully",
                }
            ),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_profile_blueprint.route("/user/address", methods=["GET"])
@jwt_required
def get_user_profile_address():
    """
    Get user data if available
    """
    user = get_user_for_token_identity()
    if user:
        if user.address:
            return user.address.to_json(), 200
        return dumps({}), 200
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_profile_blueprint.route("/user/address", methods=["POST"])
@jwt_required
def user_profile_address():
    """
    Save user data
    """
    user = get_user_for_token_identity()
    if user:
        data = request.json
        if user.address:
            user.address.update_address_from_web_data(data)
            return user.address.to_json(), 200
        # else continue
        address = Address.create_address_from_web_data(data)
        user.address = address
        user.save()
        return dumps(address), 200
    return dumps({"ok": False, "message": "Invalid user"}), 400
