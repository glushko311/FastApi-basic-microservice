from typing import Union
from pydantic import BaseModel


class ItemCreateSchema(BaseModel):
    number: Union[str, None] = None
    title: str
    description: Union[str, None] = None
    location: Union[str, None] = None
    public: bool
    marked: bool
    collection_id: int


class ItemShortSchema(BaseModel):
    number: Union[str, None] = None
    title: str
    location: Union[str, None] = None


class ItemUpdateSchema(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    marked: Union[bool, None] = None

