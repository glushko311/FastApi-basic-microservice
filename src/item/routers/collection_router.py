import typing

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config import VERSION_PREFIX
from src.auth.managers import UserManager
from src.auth.schemas import UserSchema
from src.item.managers import CollectionManager
from src.item.schemas import CollectionCreateSchema, CollectionSchema
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.item.schemas.item_schema import ItemShortSchema

collection_router = APIRouter(
    prefix=f"{VERSION_PREFIX}/collection",
    tags=["collection"]
)


@collection_router.post("", response_model=CollectionCreateSchema)
async def add_collection(
        collection_data: CollectionCreateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user)
):
    collection = await CollectionManager.create_collection(
        db=db,
        user_id=current_user.id,
        collection_data=collection_data
    )
    return JSONResponse(content=jsonable_encoder(collection))


@collection_router.put("", response_model=CollectionSchema)
async def update_collection(
        collection_id: int,
        collection_data: CollectionCreateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user),
):
    collection = await CollectionManager.update_collection(
        db=db,
        collection_id=collection_id,
        collection_data=collection_data,
        user_id=current_user.id
    )
    return JSONResponse(content=jsonable_encoder(collection))


@collection_router.get("",  response_model=typing.Iterable[CollectionSchema])
async def get_user_collections(
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user)
):
    collections = await CollectionManager.get_collections_by_user(
        db=db, user_id=current_user.id
    )
    return JSONResponse(content=jsonable_encoder(collections))


@collection_router.get("{collection_id}", response_model=typing.Iterable[ItemShortSchema])
async def get_collection_items(
        collection_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user),

):
    collection_items = await CollectionManager.get_collection_items(
        db=db,
        user_id=current_user.id,
        collection_id=collection_id
    )

    return JSONResponse(content=jsonable_encoder(collection_items))


@collection_router.delete("")
async def delete_by_id(
        collection_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user),

):
    if await CollectionManager.delete_collection_by_id(
        db=db,
        user_id=current_user.id,
        collection_id=collection_id
    ):
        return {"detail": "collection deleted"}
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="something wents wrong, collection not deleted"
    )
