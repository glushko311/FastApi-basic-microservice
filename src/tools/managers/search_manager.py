import typing


if typing.TYPE_CHECKING:
    # from src.item.schemas import ItemCreateSchema, ItemUpdateSchema
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.item.models import Item
    from src.item.models import Tag


class SearchManager:

    @staticmethod
    async def search_tags(db: 'AsyncSession', search_string: str)-> typing.Iterable['Tag']:
        ...

    @staticmethod
    async def search_items_by_tag(db: 'AsyncSession', search_string: str) -> typing.Iterable['Item']:
        ...

    @staticmethod
    async def search_items_by_title(db: 'AsyncSession', search_string: str) -> typing.Iterable['Item']:
        ...

    @staticmethod
    async def search_items_by_description(db: 'AsyncSession', search_string: str) -> typing.Iterable['Item']:
        ...
