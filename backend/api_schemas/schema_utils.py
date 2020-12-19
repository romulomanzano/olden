import datetime


def coerce_date_to_string(_date):
    return _date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def coerce_into_datetime(datetime_string):
    return datetime.strptime(datetime_string, "YYYY-MM-DDTHH:mm[Z]")
