import pytz
from datetime import datetime, timedelta

class DatetimeUtil:
    @staticmethod
    def get_local_datetime() -> datetime:
        return datetime.now(pytz.timezone('Asia/Bangkok'))
    
    @staticmethod
    def get_expiration_time(minutes: int) -> datetime:
        return datetime.now() + timedelta(minutes=minutes)
