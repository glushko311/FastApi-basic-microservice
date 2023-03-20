import datetime
import typing

from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import delete, and_

from src.item.models import Tag

if typing.TYPE_CHECKING:
    from src.item.schemas import TagSchema
    from sqlalchemy.ext.asyncio import AsyncSession


class TagManager:
    @staticmethod
    async def get_all_user_tags(db: 'AsyncSession', user_id: int) -> typing.List['TagSchema']:
        query = await db.execute(
            select(Tag.id, Tag.title, Tag.created_by).
            where(Tag.created_by == user_id)
        )
        tags = query.all()
        return tags

    @staticmethod
    async def create_tag(db: 'AsyncSession', user_id: int, tag_title: str) -> 'TagSchema':
        title = tag_title.lower()
        query = await db.execute(
            select(Tag.id).filter(Tag.title == title)
        )
        is_tag_already_exists = query.scalar()
        if is_tag_already_exists:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Tag \"{title}\" already exists."
            )
        new_tag = Tag(
            title=title,
            created=datetime.datetime.utcnow(),
            created_by=user_id,
        )
        db.add(new_tag)
        await db.commit()
        await db.refresh(new_tag)
        return new_tag

    @staticmethod
    async def delete_tag(db: 'AsyncSession', tag_id: int, user_id: int) -> bool:
        tag_get_query = await db.execute(
            select(Tag).where(and_(Tag.id == tag_id, Tag.created_by == user_id))
        )
        tag = tag_get_query.scalar()
        if tag:
            await db.delete(tag)
            await db.commit()
            return True
        return False


    @staticmethod
    async def find_tags_by_part_of_title(
            db: 'AsyncSession',
            tag_title_part: str,
            user_id: int,
            only_my: bool = False,
    ) -> typing.Iterable['TagSchema']:

        tag_title_part = tag_title_part.lower()
        select_query = select(Tag.id, Tag.title).filter(Tag.title.like(f'%{tag_title_part}%'))
        if only_my:
            select_query = select_query.filter(Tag.created_by == user_id)
        query = await db.execute(select_query)
        tags = query.all()
        return tags
