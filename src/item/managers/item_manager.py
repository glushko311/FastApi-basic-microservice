import datetime
import typing

from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import delete, and_

from src.item.models import Item
from src.item.managers import CollectionManager
from src.item.schemas.item_schema import ItemShortSchema

if typing.TYPE_CHECKING:
    from src.item.schemas import ItemCreateSchema, ItemUpdateSchema
    from sqlalchemy.ext.asyncio import AsyncSession


class ItemManager:
    @staticmethod
    async def get_items_by_user(db: 'AsyncSession', user_id: int) -> typing.List[ItemShortSchema]:
        query = await db.execute(
            select(Item.id, Item.number, Item.title, Item.location, Item.user).
            where(Item.user_id == user_id).
            limit(5).
            offset(0)
        )
        items = query.all()
        return items

    @staticmethod
    async def get_item_by_id(db: 'AsyncSession', item_id: int, user_id: int) -> Item:
        query = await db.execute(
            select(Item)
            .where(Item.id == item_id)
            .filter(Item.user_id == user_id)
        )
        item = query.scalar()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id={item_id} not found or you are not an owner of it"
            )
        return item

    @staticmethod
    async def create_item(db: 'AsyncSession', user_id: int, item_data: 'ItemCreateSchema') -> Item:
        is_collection = await CollectionManager.check_is_collection_exists_and_owner(
                db=db, owner_id=user_id, collection_id=item_data.collection_id
        )
        if not is_collection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection not found, or you not an owner of it"
            )

        item: Item = Item(
            number=item_data.number,
            title=item_data.title,
            description=item_data.description,
            location=item_data.location,
            created=datetime.datetime.utcnow(),
            public=item_data.public,
            disabled=False,
            marked=item_data.marked,
            user_id=user_id,
            collection_id=item_data.collection_id
        )

        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @classmethod
    async def update_item(
            cls,
            db: 'AsyncSession',
            item_data: 'ItemUpdateSchema',
            user_id: int,
            item_id: int,
    ) -> Item:
        item: Item = await cls.get_item_by_id(
            db=db, user_id=user_id, item_id=item_id
        )
        item.title = item_data.title or item.title
        item.description = item_data.description or item.description
        if item_data.marked is not None:
            item.marked = item_data.marked
        await db.commit()
        return item

    @staticmethod
    async def del_items_by_id(db: 'AsyncSession', items: typing.Iterable[int], user_id: int) -> bool:
        await db.execute(delete(Item).where(and_(Item.id.in_(items), Item.user_id == user_id)))
        await db.commit()
        return True
