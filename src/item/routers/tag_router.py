import typing

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config import VERSION_PREFIX
from src.auth.managers import UserManager
from src.auth.schemas import UserSchema
from src.item.managers.tag_manager import TagManager
from src.item.schemas import TagCreateSchema, TagSchema
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


tag_router = APIRouter(
    prefix=f"{VERSION_PREFIX}/tag",
    tags=["tag"]
)


@tag_router.post("", response_model=TagCreateSchema)
async def add_tag(
        tag_data: TagCreateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user)
):
    tag = await TagManager.create_tag(db=db, user_id=current_user.id, tag_title=tag_data.title)
    return JSONResponse(content=jsonable_encoder(tag))


@tag_router.get("",  response_model=typing.Iterable[TagCreateSchema])
async def get_all_user_tag(
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user)
):
    tags = await TagManager.get_all_user_tags(db=db, user_id=current_user.id)
    return JSONResponse(content=jsonable_encoder(tags))


@tag_router.get("/search",  response_model=typing.Iterable[TagSchema])
async def get_all_tags_by_part(
        tag_title_part: str,
        db: AsyncSession = Depends(get_session),
        only_my: bool = False,
        current_user: UserSchema = Depends(UserManager.get_current_active_user)
):
    tags = await TagManager.find_tags_by_part_of_title(
        db=db,
        only_my=only_my,
        user_id=current_user.id,
        tag_title_part=tag_title_part
    )
    return JSONResponse(content=jsonable_encoder(tags))


@tag_router.delete("")
async def delete_tag_by_id(
        tag_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserSchema = Depends(UserManager.get_current_active_user),

):
    if await TagManager.delete_tag(
        db=db,
        user_id=current_user.id,
        tag_id=tag_id
    ):
        return {"detail": "tag deleted"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="tag not found, or user not have permissions"
    )