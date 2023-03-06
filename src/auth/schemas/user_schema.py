from typing import Union
from pydantic import BaseModel

from src.auth.schemas.role_schema import RoleSchema


class UserSchema(BaseModel):
    id: int
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    hashed_password: str
    session: Union[bool, None] = None
    role: RoleSchema


class UserRegSchema(BaseModel):
    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
