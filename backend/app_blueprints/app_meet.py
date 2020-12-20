""""Module to house the auth related endpoints"""
from flask import Blueprint, request
from models import VirtualEvent
from flask_cors import CORS
from bson.json_util import dumps
import config

# define the blueprint variable
app_meet_blueprint = Blueprint("app_meet", __name__)
# allow for cross site origins
cors = CORS(app_meet_blueprint, origins=config.WEB_ONLY_CORS_ORIGINS)


@app_meet_blueprint.route("/redirect", methods=["GET"])
def get_redirect_url():
    """
    Get user data if available
    """
    data = request.args
    meeting = VirtualEvent.objects(internal_url=data.get("meetingUrl")).first()
    if meeting:
        return (
            dumps({"ok": True, "meeting_url": meeting.meeting_details.url}),
            200,
        )
    return dumps({"ok": False, "message": "Meeting not found"}), 400
