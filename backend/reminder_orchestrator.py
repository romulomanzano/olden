from models import VirtualEvent
from utils import logged
from communications.communications import Notifier
from communications import communications_mapping
import datetime
from dateutil.relativedelta import relativedelta
import argparse


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
        threshold_timestamp = self.now + relativedelta(minutes=self.minutes_from_now)
        self.logger.info("{} - {}".format(self.now, threshold_timestamp))
        upcoming_events = VirtualEvent.objects(
            canceled__ne=True, date__gt=self.now, date__lte=threshold_timestamp
        )
        self.logger.info(
            "Sending reminders for {} upcoming events".format(upcoming_events.count())
        )
        for event in upcoming_events:
            if self.reminder_name not in event.reminders_sent:
                for attendee in event.attendees:
                    try:
                        notifier.notify(
                            comms_name=self.reminder_name,
                            recipient_id=str(attendee.id),
                            data={
                                "event_name": event.name,
                                "organization_name": event.organization.name,
                                "first_name": attendee.first_name,
                                "meeting_url": event.meeting_details.url,
                            },
                            profile=attendee.contact_profile,
                            idempotency_key=None,
                        )
                    except Exception as e:  # skipcq: PYL-W0703
                        self.logger.exception(e)
                event.reminders_sent.append(self.reminder_name)
                event.save()
            self.logger.info(
                "{} reminders sent for {}".format(self.reminder_name, str(event.id))
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--action",
        help="Choose what action to take",
        required=True,
        choices=[
            "remind",
        ],
    )

    parser.add_argument(
        "--reminder-name",
        help="Choose reminder name",
        required=True,
        choices=["upcoming_event_one_hour", "upcoming_event_five_minutes"],
        dest="reminder_name",
    )

    args = parser.parse_args()
    if args.action == "remind":
        if args.reminder_name == "upcoming_event_one_hour":
            rm = ReminderOrchestrator(
                communications_mapping.EVENT_REMINDER_1HR_BEFORE, 60
            )
            rm.send_reminders()
        elif args.reminder_name == "upcoming_event_five_minutes":
            rm = ReminderOrchestrator(
                communications_mapping.EVENT_REMINDER_5MINS_BEFORE, 5
            )
            rm.send_reminders()
