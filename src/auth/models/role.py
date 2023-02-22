from src.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    permissions = Column(JSON)


