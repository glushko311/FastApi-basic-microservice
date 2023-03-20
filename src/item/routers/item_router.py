import typing

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config import VERSION_PREFIX
from src.auth.managers import UserManager
from src.auth.schemas import UserSchema
from src.item.managers import ItemManager
from src.item.schemas import ItemCreateSchema
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.item.schemas.item_schema import ItemShortSchema, ItemUpdateSchema

item_router = APIRouter(
    prefix=f"{VERSION_PREFIX}/item",
    tags=["item"]
)


@item_router.post("", response_model=ItemCreateSchema)
async def add_item(
        item_data: ItemCreateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user)
):
    item = await ItemManager.create_item(db=db, user_id=current_user.id, item_data=item_data)
    return JSONResponse(content=jsonable_encoder(item))


@item_router.put("", response_model=ItemCreateSchema)
async def update_item(
        item_id: int,
        item_data: ItemUpdateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user),
):
    updated_item = await ItemManager.update_item(
        db=db,
        item_id=item_id,
        item_data=item_data,
        user_id=current_user.id
    )
    return JSONResponse(content=jsonable_encoder(updated_item))


@item_router.get("",  response_model=typing.Iterable[ItemShortSchema])
async def read_own_items(
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user)
):
    items = await ItemManager.get_items_by_user(db=db, user_id=current_user.id)
    return JSONResponse(content=jsonable_encoder(items))


@item_router.get("{item_id}", response_model=ItemCreateSchema)
async def read_item_by_id(
        item_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user),

):
    item = await ItemManager.get_item_by_id(
        db=db,
        user_id=current_user.id,
        item_id=item_id
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return JSONResponse(content=jsonable_encoder(item))


@item_router.delete("")
async def read_item_by_id(
        item_ids: typing.Iterable[int],
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user),

):
    if await ItemManager.delete_items_by_id(
        db=db,
        user_id=current_user.id,
        items=item_ids
    ):
        return {"detail": "items deleted"}
    return {"detail": "items deleted"}