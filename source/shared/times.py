import datetime


def get_utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)
