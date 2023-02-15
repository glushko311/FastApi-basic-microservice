import typing

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_PORT, DB_PASS, DB_NAME, DB_USER


if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine

DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine: 'AsyncEngine' = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session: sessionmaker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
