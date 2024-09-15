from typing import Any, Optional
import jwt

from utils.datetime_util import DatetimeUtil
from configs.app_config import appConfig

ALGORITHM = "HS256" # Algorithm for encoding and decoding JWT

class JwtUtil:
    @staticmethod
    def create(payload: dict[str, Any]) -> str:
        expiration = DatetimeUtil.get_expiration_time(appConfig.JWT_EXPIRE_MINUTES)
        payload.update({"exp": expiration})
        
        token = jwt.encode(payload, appConfig.JWT_SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def decode(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, appConfig.JWT_SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError as e:
            return e
        except jwt.InvalidTokenError as e:
            return e
