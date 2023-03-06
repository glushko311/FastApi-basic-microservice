from sqlalchemy.orm import relationship

from src.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN


class User(Base):

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(200))
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(500), nullable=False)
    disabled = Column(BOOLEAN)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role", lazy="joined")
    session = relationship("Session", uselist=False, back_populates="user", lazy="joined")
