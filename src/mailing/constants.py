from enum import StrEnum


class SendingStatus(StrEnum):
    PENDING = 'PENDING'
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    RETRY = 'RETRY'
    FAILURE = 'FAILURE'
