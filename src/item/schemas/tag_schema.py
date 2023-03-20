from pydantic import BaseModel


class TagCreateSchema(BaseModel):
    title: str


class TagSchema(BaseModel):
    id: int
    title: str
    created_by: int
