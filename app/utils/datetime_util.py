import pytz
from datetime import datetime

# Function to get local datetime in Thailand timezone


def get_local_datetime() -> datetime:
    return datetime.now(pytz.timezone('Asia/Bangkok'))
