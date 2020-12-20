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
    "meeting_details": {
        "type": "dict",
        "schema": {
            "_id": {"type": "string"},
            "name": {"type": "string", "nullable": True},
            "api_created": {"type": "boolean", "nullable": True},
            "privacy": {"type": "string", "nullable": True},
            "url": {"type": "string"},
            "created_at": {
                "type": "string",
                "coerce": coerce_date_to_string,
            },
            "config": {
                "type": "dict",
                "schema": {
                    "start_audio_off": {"type": "boolean", "nullable": True},
                    "start_video_off": {"type": "boolean", "nullable": True},
                    "exp": {
                        "type": "string",
                        "coerce": coerce_date_to_string,
                    },
                    "nbf": {
                        "type": "string",
                        "coerce": coerce_date_to_string,
                    },
                    "max_participants": {"type": "integer", "nullable": True},
                    "eject_after_elapsed": {"type": "integer", "nullable": True},
                    "eject_at_room_exp": {"type": "boolean", "nullable": True},
                    "lang": {"type": "string", "nullable": True},
                },
            },
        },
    },
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
