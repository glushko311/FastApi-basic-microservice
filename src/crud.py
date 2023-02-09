import typing

from sqlalchemy.orm import Session

from src.models import User
from src.schemas import User as UserSchema


# def get_user_by_lastname(db: Session, lastname: str):
#     result = db.query(User).filter(User.last_name == lastname).first()
#     if not result:
#         return None
#     return result
#
#
# def create_user(db: Session, user: UserSchema):
#     user: User = User(
#         first_name=user.first_name,
#         last_name=user.last_name,
#         phone_number=user.phone_number,
#         age=user.age
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user
