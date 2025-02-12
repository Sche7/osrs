from enum import Enum


class BotoErrorCode(str, Enum):
    NO_SUCH_KEY = "NoSuchKey"
    ENTITY_ALREADY_EXISTS = "EntityAlreadyExists"
