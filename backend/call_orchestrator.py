import requests
import config
from dateutil.relativedelta import relativedelta
from utils import logged
import cerberus
from api_schemas.meeting_details_schema import meeting_response_schema
from api_schemas.schema_utils import datetime_to_unix
import secrets


@logged
class CallOrchestrator:
    def __init__(self):
        self.base_url = config.DAILY_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(config.DAILY_API_KEY),
        }

    def create_room(
        self,
        start_datetime,
        duration_estimate_minutes,
        eject_at_room_exp=True,
        max_participants=20,
        lang=config.MEETING_DEFAULT_LANGUAGE,
        name=None,
    ):
        name = name or "{}{}".format(
            config.MEETING_ROOM_DEFAULT_PREFIX, secrets.token_hex(3)
        )
        expire_after_minutes = (
            duration_estimate_minutes or 60
        ) + 10  # add a buffer of 10 minutes
        early_join_buffer_minutes = 5
        not_before = datetime_to_unix(
            start_datetime - relativedelta(minutes=early_join_buffer_minutes)
        )  # 5 mins before
        expire_at = datetime_to_unix(
            start_datetime + relativedelta(minutes=expire_after_minutes)
        )
        expire_after_elapsed = (expire_after_minutes + early_join_buffer_minutes) * 60
        # see https://docs.daily.co/reference#room-configuration
        data = {
            "name": name,
            "properties": {
                "nbf": not_before,  # not before
                "max_participants": max_participants,
                "exp": expire_at,
                "eject_after_elapsed": expire_after_elapsed,  # may be redundant
                "eject_at_room_exp": eject_at_room_exp,
                "lang": lang,
            },
        }
        url = "{}/v1/rooms".format(self.base_url)
        response = requests.post(
            url,
            json=data,
            headers=self.headers,
        )

        # save response
        rjson = response.json()
        meeting_details = {
            "_id": rjson.get("id"),
            "name": rjson.get("name"),
            "api_created": rjson.get("api_created"),
            "privacy": rjson.get("privacy"),
            "url": rjson.get("url"),
            "created_at": rjson.get("created_at"),
            "config": rjson.get("config"),
        }
        normalizer = cerberus.Validator(meeting_response_schema, purge_unknown=True)
        meeting_details_normalized = normalizer.normalized(meeting_details)
        return meeting_details_normalized

    def create_permanent_room(
        self,
        kick_out_after_minutes=60,
        max_participants=20,
        lang=config.MEETING_DEFAULT_LANGUAGE,
        name=None,
    ):
        name = name or "{}{}".format(
            config.MEETING_ROOM_DEFAULT_PREFIX, secrets.token_hex(3)
        )
        expire_after_elapsed = kick_out_after_minutes
        # see https://docs.daily.co/reference#room-configuration
        data = {
            "name": name,
            "properties": {
                "max_participants": max_participants,
                "eject_after_elapsed": expire_after_elapsed,
                "lang": lang,
            },
        }
        url = "{}/v1/rooms".format(self.base_url)
        response = requests.post(
            url,
            json=data,
            headers=self.headers,
        )

        # save response
        rjson = response.json()
        meeting_details = {
            "_id": rjson.get("id"),
            "name": rjson.get("name"),
            "api_created": rjson.get("api_created"),
            "privacy": rjson.get("privacy"),
            "url": rjson.get("url"),
            "created_at": rjson.get("created_at"),
            "config": rjson.get("config"),
        }
        normalizer = cerberus.Validator(meeting_response_schema, purge_unknown=True)
        meeting_details_normalized = normalizer.normalized(meeting_details)
        return meeting_details_normalized
