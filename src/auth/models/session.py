from datetime import datetime, timedelta
import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, delete

if typing.TYPE_CHECKING:
    from src.auth import User


class Session(Base):

    __tablename__ = "session"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, nullable=False)
    expired_time = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="session")








