import typing
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession


from src.database import get_session
from src.models.user import User
from src.schemas import TokenData
from src.schemas import User as UserSchema
from config import JWT_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_TOKEN_ALGORITHM
#
# JWT_TOKEN_ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UnathorizedException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.headers = {"WWW-Authenticate": "Bearer"}
        self.detail = detail,


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(db: AsyncSession, username: str, password: str) -> typing.Union[User, bool]:

    user: User = await User.get_by_username(db, username)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_TOKEN_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)):

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_TOKEN_ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise UnathorizedException()
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise UnathorizedException(detail="Token expired")
    except JWTError:
        raise UnathorizedException()
    user: User = await User.get_by_username(db, username=token_data.username)
    if user is None:
        raise UnathorizedException()
    if user.session is None:
        raise UnathorizedException(detail="Do not have active session")
    if user.session.token != token:
        raise UnathorizedException(detail="Token invalid")
    return user


async def get_current_active_user(current_user: UserSchema = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user
