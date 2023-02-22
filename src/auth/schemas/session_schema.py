import datetime
from pydantic import BaseModel


class SessionSchema(BaseModel):
    token: str
    expired_time: datetime.datetime
    user_id: int
