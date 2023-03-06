from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    created = Column(TIMESTAMP, nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'))