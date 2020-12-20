from .schema_utils import coerce_date_to_string, coerce_into_datetime

oid_schema = {"$oid": {"type": "string"}}

event_base_schema = {
    "_id": {"schema": oid_schema},
    "name": {"type": "string"},
    "date": {"type": "string", "coerce": coerce_date_to_string},
    "original_timezone_name": {"type": "string"},
    "created_by": {"schema": oid_schema},
    "created_date": {"type": "string", "coerce": coerce_date_to_string},
    "canceled": {"type": "boolean"},
    "canceled_date": {"type": "string", "coerce": coerce_date_to_string},
    "canceled_by": {"schema": oid_schema},
}


event_list_schema = {
    "events": {
        "type": "list",
        "schema": {"type": "dict", "schema": event_base_schema},
    }
}


event_input_schema = {
    "eventName": {"type": "string"},
    "eventDatetime": {"type": "datetime", "coerce": coerce_into_datetime},
}
