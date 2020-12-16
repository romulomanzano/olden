""""Module to house the utils related endpoints"""
import config as config
import constants as constants
from flask import Blueprint
from models import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_cors import CORS
from bson.json_util import dumps
import utils
import mongoengine

logger = utils.get_generic_logger(__name__)

# define the blueprint variable
app_utils_blueprint = Blueprint("app_utils", __name__)
# allow for cross site origins
cors = CORS(app_utils_blueprint, origins=config.WEB_ONLY_CORS_ORIGINS)


@app_utils_blueprint.route("/states/us", methods=["GET"])
@jwt_required
def get_list_of_states_us():
    """ Register a new user endpoint """
    return dumps(constants.US_STATES), 200


def get_user_for_token_identity():
    """
    Get user for identity
    """
    identity = get_jwt_identity()
    try:
        user = User.objects.get(id=identity["id"])
        return user
    except mongoengine.DoesNotExist as e:
        logger.error("Error loading identity: {}".format(e))
