"""
API to interact with email services (via courier)
"""
from config import COURIER_API_TOKEN
import utils
from trycourier import Courier
from .communications_mapping import COMMS_TO_EVENT_MAP


@utils.logged
class Notifier:
    def __init__(self):
        self.client = Courier(auth_token=COURIER_API_TOKEN)

    def notify(
        self, comms_name, recipient_id, data, profile=None, idempotency_key=None
    ):
        """Send communications via courier"""
        event_id = COMMS_TO_EVENT_MAP[comms_name]
        resp = self.client.send(
            event=event_id,
            recipient=recipient_id,
            data=data,
            profile=profile,
            idempotency_key=idempotency_key,
        )
        return resp

    def replace_or_create_profile(self, recipient_id, profile):
        """Create or replace profile"""
        resp = self.client.replace_profile(recipient_id, profile)
        return resp

    def update_or_create_profile(self, recipient_id, profile):
        """Create or update profile"""
        resp = self.client.merge_profile(recipient_id, profile)
        return resp
