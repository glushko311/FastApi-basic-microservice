from sqlalchemy.orm import relationship

from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, delete, BOOLEAN, JSON, Table


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    location = Column(String(50), unique=False, nullable=False)
    created = Column(TIMESTAMP, nullable=False)
    public = Column(BOOLEAN, nullable=False)
    disabled = Column(BOOLEAN, nullable=False)
    marked = Column(BOOLEAN, nullable=False)
    pictures = relationship("Picture", uselist=True, back_populates="item", lazy="joined")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", lazy="joined")
    collection_id = Column(Integer, ForeignKey('collection.id'))
    tags = relationship('Tag', secondary='item_tag_association', back_populates='items', lazy="joined")



