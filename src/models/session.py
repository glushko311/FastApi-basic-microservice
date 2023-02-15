from datetime import datetime, timedelta
import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, delete

if typing.TYPE_CHECKING:
    from src.models import User


class Session(Base):

    __tablename__ = "session"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    expired_time = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="session")

    @staticmethod
    async def update_session(db: AsyncSession, user: 'User', token: str):

        if user.session:
            await db.execute(delete(Session).where(Session.user_id == user.id))

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








