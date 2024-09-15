import pytz
from datetime import datetime

class DatetimeUtil:
    @staticmethod
    def get_local_datetime() -> datetime:
        return datetime.now(pytz.timezone('Asia/Bangkok'))
