""""Module to house the emergency related endpoints"""
import config
from flask import Blueprint, request
from models import VirtualEvent, Member, Organization
from flask_jwt_extended import jwt_required
from flask_cors import CORS
from app_utils import get_user_for_token_identity
from utils import get_generic_logger
from bson.json_util import dumps
from bson import ObjectId
import bson
from api_schemas.virtual_event_schemas import event_list_schema, event_input_schema
import cerberus
import datetime

# define the blueprint variable
app_organization_blueprint = Blueprint("app_virtual_events", __name__)
# allow for cross site origins
cors = CORS(app_organization_blueprint, origins=config.API_CORS_ORIGINS)
logger = get_generic_logger(__name__)


def get_organization_if_user_is_admin(org_id, user):
    org = Organization.objects(id=ObjectId(org_id)).first()
    if org in user.organizations:
        return org
    return


@app_organization_blueprint.route("/<org_id>/virtual_events", methods=["GET"])
@jwt_required
def get_user_virtual_events(org_id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        # specific mongo query
        events = VirtualEvent.get_organization_events(org)
        normalizer = cerberus.Validator(event_list_schema, purge_unknown=True)
        event_list = normalizer.normalized(
            {"events": [x.to_mongo().to_dict() for x in events]}
        )
        return (dumps(event_list), 200)
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route("/<org_id>/virtual_events/add", methods=["POST"])
@jwt_required
def add_new_virtual_event(org_id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        data = request.json
        normalizer = cerberus.Validator(event_input_schema, purge_unknown=False)
        event_input = normalizer.normalized(data)
        event = VirtualEvent.create(
            name=event_input.get("eventName"),
            date=event_input.get("eventDatetime"),
            created_date=datetime.datetime.utcnow(),
            created_under_timezone=event_input.get("createdUnderTimezone"),
            created_by=user,
            organization=org,
        )
        return (
            dumps(
                {
                    "ok": True,
                    "message": "Event created successfully",
                    "virtual_event": event.to_mongo().to_dict(),
                }
            ),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route(
    "/<org_id>/virtual_events/<_id>/attendees", methods=["GET"]
)
@jwt_required
def get_attendees_to_virtual_event(org_id, _id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        if not bson.objectid.ObjectId.is_valid(_id):
            return dumps({"ok": False, "message": "Invalid Event Id"}), 420
        event = VirtualEvent.objects(_id=ObjectId(_id), organization=org).first()
        if not event:
            logger.error("Can't retrieve event id {}".format(_id))
            return (
                dumps({"ok": False, "message": "No event found with that id"}),
                420,
            )
        return (
            dumps(
                {
                    "ok": True,
                    "attendee_list": [x.to_mongo().to_dict() for x in event.attendees],
                }
            ),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route("/<org_id>/virtual_events/<_id>", methods=["GET"])
@jwt_required
def get_virtual_event(org_id, _id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        if not bson.objectid.ObjectId.is_valid(_id):
            return dumps({"ok": False, "message": "Invalid Event Id"}), 420
        event = VirtualEvent.objects(_id=ObjectId(_id), organization=org).first()
        if not event:
            logger.error("Can't retrieve event id {}".format(_id))
            return (
                dumps({"ok": False, "message": "No event found with that id"}),
                420,
            )
        return dumps({"ok": True, "event": event.to_mongo().to_dict()}), 200
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route(
    "/<org_id>/virtual_events/<_id>/attendees/add", methods=["POST"]
)
@jwt_required
def add_attendees_to_virtual_event(org_id, _id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        if not bson.objectid.ObjectId.is_valid(_id):
            return dumps({"ok": False, "message": "Invalid Event Id"}), 420
        event = VirtualEvent.objects(_id=ObjectId(_id), organization=org).first()
        if not event:
            logger.error("Can't retrieve event id {}".format(_id))
            return (
                dumps({"ok": False, "message": "No event found with that id"}),
                420,
            )
        data = request.json
        if data.get("addExistingMemberId"):
            member = Member.objects.get(id=ObjectId(data["addExistingMemberId"]))
        else:
            member = Member(
                first_name=data.get("userFirstName"),
                last_name=data.get("userLastName"),
                phone_number=data.get("userPhoneNumber"),
                email=data.get("userEmail"),
                organization=org,
                active=True,
            )
            member.save()

        if member in event.attendees:
            return (
                dumps(
                    {"ok": False, "message": "Attendee is already part of this event"}
                ),
                400,
            )
        event.add_attendee(member)
        return (
            dumps({"ok": True, "message": "Attendee added successfully"}),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route("/<org_id>/members/add", methods=["POST"])
@jwt_required
def add_member_organization(org_id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        data = request.json
        member = Member(
            first_name=data.get("userFirstName"),
            last_name=data.get("userLastName"),
            phone_number=data.get("userPhoneNumber"),
            email=data.get("userEmail"),
            organization=org,
            active=True,
        )
        member.save()
        return (
            dumps({"ok": True, "message": "Member added successfully"}),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route("/<org_id>/members/<_id>/archive", methods=["POST"])
@jwt_required
def archive_member_from_organization(org_id, _id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        if not bson.objectid.ObjectId.is_valid(_id):
            return dumps({"ok": False, "message": "Invalid Member Id"}), 420
        member = Member.objects(id=ObjectId(_id), organization=org, active=True).first()
        if not member:
            return dumps({"ok": False, "message": "Active member not found"}), 400
        member.mark_archived()
        return (
            dumps({"ok": True, "message": "Member marked inactive"}),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route("/<org_id>/members", methods=["GET"])
@jwt_required
def get_organiztion_members(org_id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        data = request.args
        members = Member.objects(
            organization=org, active=bool(data.get("active") == "true")
        )
        return (
            dumps({"ok": True, "members": [x.to_mongo().to_dict() for x in members]}),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route(
    "/<org_id>/virtual_events/<_id>/attendees/remove", methods=["POST"]
)
@jwt_required
def remove_attendees_from_virtual_event(org_id, _id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        if not bson.objectid.ObjectId.is_valid(_id):
            return dumps({"ok": False, "message": "Invalid Event Id"}), 420
        event = VirtualEvent.objects(id=ObjectId(_id), organization=org).first()
        if not event:
            logger.error("Can't retrieve event id {}".format(_id))
            return (
                dumps({"ok": False, "message": "No event found with that id"}),
                420,
            )
        data = request.json
        if not bson.objectid.ObjectId.is_valid(data.get("attendeeId")):
            return dumps({"ok": False, "message": "Invalid Attendee Id"}), 420
        attendee = Member.objects(id=ObjectId(data["attendeeId"])).first()
        if attendee not in event.attendees:
            return (
                dumps({"ok": False, "message": "Attendee is not part of this event"}),
                400,
            )
        event.remove_attendee(attendee)
        return (
            dumps({"ok": True, "message": "Attendee removed successfully"}),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route(
    "/<org_id>/virtual_events/<_id>/alert_settings", methods=["GET"]
)
@jwt_required
def get_event_alert_settings(org_id, _id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        if not bson.objectid.ObjectId.is_valid(_id):
            return dumps({"ok": False, "message": "Invalid Event Id"}), 420
        event = VirtualEvent.objects(id=ObjectId(_id), organization=org).first()
        if not event:
            logger.error("Can't retrieve event id {}".format(_id))
            return (
                dumps({"ok": False, "message": "No event found with that id"}),
                420,
            )
        return (dumps(event.alert_settings.to_mongo().to_dict()), 200)
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route(
    "/<org_id>/virtual_events/<_id>/cancel", methods=["POST"]
)
@jwt_required
def cancel_event(org_id, _id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        if not bson.objectid.ObjectId.is_valid(_id):
            return dumps({"ok": False, "message": "Invalid Event Id"}), 420
        event = VirtualEvent.objects(id=ObjectId(_id), organization=org).first()
        if not event:
            logger.error("Can't retrieve event id {}".format(_id))
            return (
                dumps({"ok": False, "message": "No event found with that id"}),
                420,
            )
        event.cancel(user)
        return (dumps({"ok": True, "message": "Event Successfully Canceled"}), 200)
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route(
    "/<org_id>/virtual_events/<_id>/alert_settings/update", methods=["POST"]
)
@jwt_required
def update_alert_settings(org_id, _id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        if not bson.objectid.ObjectId.is_valid(_id):
            return dumps({"ok": False, "message": "Invalid Event Id"}), 420
        event = VirtualEvent.objects(id=ObjectId(_id), organization=org).first()
        if not event:
            logger.error("Can't retrieve event id {}".format(_id))
            return (
                dumps({"ok": False, "message": "No event found with that id"}),
                420,
            )
        data = request.json
        alert_settings = data["alertSettings"]
        event.alert_settings.update(**alert_settings)
        return (
            dumps(
                {
                    "ok": True,
                    "message": "Alert settings successfully updated",
                    "alert_settings": event.alert_settings.to_mongo().to_dict(),
                }
            ),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400


@app_organization_blueprint.route("/<org_id>/account_summary", methods=["GET"])
@jwt_required
def organization_account_summary(org_id):
    user = get_user_for_token_identity()
    if user:
        org = get_organization_if_user_is_admin(org_id, user)
        if not org:
            return dumps({"ok": False, "message": "Invalid organization"}), 400
        account_summary = org.account_summary()
        return (
            dumps(
                {
                    "ok": True,
                    "upcoming_events": account_summary.get("upcoming_events"),
                    "past_events": account_summary.get("past_events"),
                    "active_members": account_summary.get("active_members"),
                }
            ),
            200,
        )
    return dumps({"ok": False, "message": "Invalid user"}), 400
