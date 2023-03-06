from src.database import Base

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, BOOLEAN


class Collection(Base):
    __tablename__ = "collection"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)
    created = Column(TIMESTAMP, nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'))
    owner = Column(Integer, ForeignKey('user.id'))
    disabled = Column(BOOLEAN, nullable=False)
