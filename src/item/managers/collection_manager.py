import datetime
import typing

from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import delete

from src.item.models import Item, Collection

if typing.TYPE_CHECKING:
    from src.item.schemas import ItemShortSchema, CollectionCreateSchema, CollectionSchema
    from sqlalchemy.ext.asyncio import AsyncSession


class CollectionManager:
    @staticmethod
    async def get_collections_by_user(db: 'AsyncSession', user_id: int) -> typing.List['CollectionSchema']:
        query = await db.execute(
            select(Collection).
            where(Collection.owner == user_id)
        )
        collections = query.all()
        return collections

    @classmethod
    async def get_collection_items(
            cls,
            db: 'AsyncSession',
            collection_id: int,
            user_id: int
    ) -> typing.Iterable['ItemShortSchema']:

        if await cls.check_is_collection_exists_and_owner(db, collection_id, user_id):
            get_items_query = await db.execute(
                select(Item.id, Item.number, Item.title, Item.location, Item.collection_id)
                .where(Item.collection_id == collection_id)
                .limit(5)
                .offset(0)
            )
            return get_items_query.unique().all()
        return []

    @staticmethod
    async def create_collection(
            db: 'AsyncSession',
            user_id: int,
            collection_data: 'CollectionCreateSchema'
    ) -> Collection:

        collection: Collection = Collection(
            title=collection_data.title,
            description=collection_data.description,
            created=datetime.datetime.utcnow(),
            created_by=user_id,
            owner=user_id,
            disabled=False,
        )
        db.add(collection)
        await db.commit()
        await db.refresh(collection)
        return collection

    @classmethod
    async def update_collection(
            cls,
            db: 'AsyncSession',
            collection_data: 'CollectionCreateSchema',
            user_id: int,
            collection_id: int,
    ) -> Collection:
        collection = await cls.get_collection_by_collection_id_and_owner_id(
            db=db, owner_id=user_id, collection_id=collection_id
        )
        collection.title = collection_data.title or collection.title
        collection.description = collection_data.description or collection.description
        await db.commit()
        return collection

    @classmethod
    async def delete_collection_by_id(
            cls,
            db: 'AsyncSession',
            collection_id: int,
            user_id: int,
    ) -> bool:

        if not await cls.check_is_collection_exists_and_owner(db, collection_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection not exists, or user not have permissions")
        items = await cls.get_collection_items(db, collection_id, user_id)
        if items:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Collection not empty, delete items first")
        await db.execute(delete(Collection).where(Collection.id == collection_id))
        await db.commit()
        return True

    @staticmethod
    async def check_is_collection_exists_and_owner(
            db: 'AsyncSession',
            collection_id: int,
            owner_id: int,
    ) -> bool:
        get_collection_query = await db.execute(select(Collection.id)
                                                .where(Collection.owner == owner_id)
                                                .filter(Collection.id == collection_id))
        return bool(get_collection_query.scalar())

    @staticmethod
    async def get_collection_by_collection_id_and_owner_id(
            db: 'AsyncSession',
            collection_id: int,
            owner_id: int,
    ) -> Collection:
        get_collection_query = await db.execute(select(Collection)
                                                .where(Collection.owner == owner_id)
                                                .filter(Collection.id == collection_id))
        collection: Collection = get_collection_query.scalar()
        if not collection:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Collection not exists or you not an owner of it")
        return collection
