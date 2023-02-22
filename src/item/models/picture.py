from datetime import datetime, timedelta
import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, delete, BOOLEAN, JSON

# if typing.TYPE_CHECKING:
#     from src.auth import User


class Picture(Base):
    __tablename__ = "picture"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    # item_id = Column(Integer, ForeignKey('item.id'))
