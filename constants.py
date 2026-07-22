from enum import StrEnum


class Messages(StrEnum):
    MISSING_REQUIRES_VAR = "missing required env var"
    CONFIG_VALUE_ERROR = "CONFIG_VALUE_ERROR"

class Fields(StrEnum):
    STANDARD_USER = "STANDARD_USER"
    PASSWORD = "PASSWORD"
    RESOURCE_URL = "RESOURCE_URL"
