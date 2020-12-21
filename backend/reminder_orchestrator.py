import requests
import config
from models import VirtualEvent
from utils import logged
import cerberus
from communications.communications import Notifier
from communications import communications_mapping
import datetime
from dateutil.relativedelta import relativedelta


@logged
class ReminderOrchestrator:
    def __init__(self, reminder_name, minutes_from_now):
        self.reminder_name = reminder_name
        self.minutes_from_now = minutes_from_now
        self.now = datetime.datetime.utcnow()

    def send_reminders(
        self,
    ):
        notifier = Notifier()
        threshold_timestamp = self.now() + relativedelta(minutes=self.minutes_from_now)
        upcoming_events = VirtualEvent.objects(
            canceled__ne=True, date_gt=self.now, date_lte=threshold_timestamp
        )
        for event in upcoming_events:
            for attendee in event.attendees:
                notifier.notify(
                    comms_name=self.reminder_name,
                    recipient_id=str(attendee.id),
                    data={
                        "event_name": None,
                        "organization_name": None,
                        "first_name": None,
                        "meeting_url": None,
                    },
                    profile=attendee.contact_profile(),
                    idempotency_key=None,
                )
