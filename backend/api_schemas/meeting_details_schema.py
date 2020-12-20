from .schema_utils import coerce_unix_timestamp_into_datetime, coerce_into_datetime

meeting_response_schema = {
    "id": {"type": "string"},
    "name": {"type": "string", "nullable": True},
    "api_created": {"type": "boolean", "nullable": True},
    "privacy": {"type": "string", "nullable": True},
    "url": {"type": "string"},
    "created_at": {"type": "datetime", "coerce": coerce_into_datetime},
    "config": {
        "type": "dict",
        "schema": {
            "start_audio_off": {"type": "boolean", "nullable": True},
            "start_video_off": {"type": "boolean", "nullable": True},
            "exp": {
                "type": "datetime",
                "coerce": coerce_unix_timestamp_into_datetime,
                "nullable": True,
            },
            "nbf": {
                "type": "datetime",
                "coerce": coerce_unix_timestamp_into_datetime,
                "nullable": True,
            },
            "max_participants": {"type": "integer", "nullable": True},
            "eject_after_elapsed": {"type": "integer", "nullable": True},
            "eject_at_room_exp": {"type": "boolean", "nullable": True},
            "lang": {"type": "string", "nullable": True},
        },
    },
}
