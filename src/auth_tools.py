from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException, status
from jose import jwt

from config import JWT_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_TOKEN_ALGORITHM


class UnathorizedException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.headers = {"WWW-Authenticate": "Bearer"}
        self.detail = detail,


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_TOKEN_ALGORITHM)
    return encoded_jwt


