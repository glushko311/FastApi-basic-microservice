from datetime import datetime, timedelta
import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import Base
from sqlalchemy import MetaData, Column, Integer, String, \
    TIMESTAMP, ForeignKey, JSON, BOOLEAN, UniqueConstraint
from fastapi import HTTPException

if typing.TYPE_CHECKING:
    from src.models import User


class Session(Base):

    __tablename__ = "session"
    # metadata = metadata
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    expired_time = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="session")

    @staticmethod
    async def add_session(db: AsyncSession, user: 'User', token: str):
        # check is session of this user exists
        # if yes del it

        if user.session:
            await db.delete(user.session)

        session: Session = Session(
            token=token,
            expired_time=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            user_id=user.id,
            user=user
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    async def update_session(self):
        pass






