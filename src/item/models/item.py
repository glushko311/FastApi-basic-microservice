from datetime import datetime, timedelta
import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, delete, BOOLEAN, JSON

# if typing.TYPE_CHECKING:
#     from src.auth import User

class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, unique=True, nullable=False)
    created = Column(TIMESTAMP, nullable=False)
    tags = Column(JSON)
    public = Column(BOOLEAN)
    disabled = Column(BOOLEAN)
    # picture_id = Column(Integer, ForeignKey('picture.id'))
    # user_id = Column(Integer, ForeignKey('user.id'))
    # User = relationship("User", lazy="joined")
    # session = relationship("Session", uselist=False, back_populates="user", lazy="joined")