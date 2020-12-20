import datetime


def coerce_date_to_string(_date):
    return _date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def coerce_into_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M%fZ")


def coerce_date_with_seconds_into_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def datetime_to_unix(date):
    return int((date - datetime.datetime(1970, 1, 1)).total_seconds())


def coerce_unix_timestamp_into_datetime(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp)
