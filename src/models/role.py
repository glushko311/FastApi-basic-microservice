import typing

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import Base
from sqlalchemy import MetaData, Column, Integer, String, \
    TIMESTAMP, ForeignKey, JSON, BOOLEAN, UniqueConstraint
# from fastapi import HTTPException

# from src.models import metadata


class Role(Base):
    __tablename__ = "role"
    # metadata = metadata
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    permissions = Column(JSON)


