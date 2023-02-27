from fastapi import Depends, APIRouter

from config import VERSION_PREFIX
from src.auth.managers import UserManager
from src.auth.schemas import UserSchema

item_router = APIRouter(
    prefix=f"{VERSION_PREFIX}/item",
    tags=["item"]
)


@item_router.get("")
async def read_own_items(current_user: UserSchema = Depends(UserManager.get_current_active_user)):
    if current_user.role.name == 'admin':
        return [{"role": 'admin'}]
    if current_user.role.name == 'user':
        return [{"role": 'user'}]
    return [{"item_id": "Foo", "owner": current_user.username}]
