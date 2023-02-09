import typing

from src.db import Base
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import Session

metadata = MetaData()

if typing.TYPE_CHECKING:
    from schemas import User as UserSchema


class User(Base):
    __tablename__ = "user"
    metadata = metadata
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    age = Column(Integer)

    @staticmethod
    def get_user_by_lastname(db: Session, lastname: str):
        result = db.query(User).filter(User.last_name == lastname).first()
        if not result:
            return None
        return result

    @staticmethod
    def create_user(db: Session, user: 'UserSchema'):
        user: User = User(
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            age=user.age
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


