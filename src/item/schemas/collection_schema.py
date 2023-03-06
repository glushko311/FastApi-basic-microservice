import datetime
from typing import Union
from pydantic import BaseModel


class CollectionCreateSchema(BaseModel):
    title: str
    description: Union[str, None] = None


class CollectionSchema(BaseModel):
    id: int
    title: str
    description: Union[str, None] = None
    created: datetime.datetime
    created_by: int
    owner: int
    disabled: bool

