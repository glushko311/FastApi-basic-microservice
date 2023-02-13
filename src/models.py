import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# from src.db import Base
from src.database import Base
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, BOOLEAN
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

metadata = MetaData()

if typing.TYPE_CHECKING:
    from schemas import UserRegSchema


class User(Base):
    __tablename__ = "user"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    full_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    disabled = Column(BOOLEAN)

    # def verify_password(self, password):
    #     return bcrypt.verify(password, self.password_hash)
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str):
        query = await db.execute(select(User).where(User.username == username))
        user = query.scalars().first()
        # user = await db.execute(select(User).where(User.username == username))
        return user

    @staticmethod
    async def get_by_email(db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    async def create_user(db: AsyncSession, user: 'UserRegSchema'):
        from src.app import get_password_hash
        user: User = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=False,
            hashed_password=get_password_hash(user.password)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
