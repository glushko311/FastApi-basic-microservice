from typing import Union, Optional
from pydantic import BaseModel, validator, root_validator, ValidationError


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Role(BaseModel):
    name: Union[str, None] = None


class Session(BaseModel):
    token: str
    # expired_time :TIMESTAMP
    user_id: int


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    hashed_password: str
    session: Union[bool, None] = None
    role: Role


class UserRegSchema(BaseModel):
    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None


