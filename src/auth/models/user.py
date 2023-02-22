import typing

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from src.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN
from fastapi import HTTPException


if typing.TYPE_CHECKING:
    from src.schemas import UserRegSchema


class UsernameNotUniqueException(HTTPException):
    pass


class EmailNotUniqueException(HTTPException):
    pass


class User(Base):

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(BOOLEAN)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role", lazy="joined")
    session = relationship("Session", uselist=False, back_populates="user", lazy="joined")

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str):
        query = await db.execute(
            select(User).where(User.username == username)
        )
        user = query.scalar()
        return user

    @staticmethod
    async def create_user(db: AsyncSession, user: 'UserRegSchema'):
        from src.auth_tools import get_password_hash
        user: User = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=False,
            hashed_password=get_password_hash(user.password),
            role_id=2
        )
        await user.check_is_email_username_unique(db)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def check_is_email_username_unique(self, db: AsyncSession):
        email_check_query = \
            await db.execute(select(User.email).where(User.email == self.email))
        username_check_query = \
            await db.execute(select(User.username).where(User.username == self.username))
        if email_check_query.scalars().first():
            raise EmailNotUniqueException(status_code=400, detail="email not unique")
        if username_check_query.scalars().first():
            raise UsernameNotUniqueException(status_code=400, detail="username not unique")
