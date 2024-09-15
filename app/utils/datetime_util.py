import pytz
from datetime import datetime


def get_local_datetime() -> datetime:
    return datetime.now(pytz.timezone('Asia/Bangkok'))
