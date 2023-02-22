from typing import Union
from pydantic import BaseModel


class RoleSchema(BaseModel):
    name: Union[str, None] = None
