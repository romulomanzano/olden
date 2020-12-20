import requests
import config
from dateutil.relativedelta import relativedelta
from utils import logged
import cerberus
from api_schemas.meeting_details_schema import meeting_response_schema


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
    ):
        expire_after_minutes = (
            duration_estimate_minutes or 60
        ) + 10  # add a buffer of 10 minutes
        early_join_buffer_minutes = 5
        not_before = (
            start_datetime - relativedelta(minutes=early_join_buffer_minutes)
        ).total_seconds()  # 5 mins before
        expire_at = (
            start_datetime + relativedelta(minutes=expire_after_minutes)
        ).total_seconds()
        expire_after_elapsed = (expire_after_minutes + early_join_buffer_minutes) * 60
        # see https://docs.daily.co/reference#room-configuration
        data = {
            "nbf": not_before,  # not before
            "max_participants": max_participants,
            "exp": expire_at,
            "eject_after_elapsed": expire_after_elapsed,  # may be redundant
            "eject_at_room_exp": eject_at_room_exp,
            "lang": lang,
        }
        url = "{}/v1/rooms".format(self.base_url)
        response = requests.request("POST", url, headers=self.headers, data=data)
        self.logger.info(response.text)
        self.logger.info(response.json())
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
