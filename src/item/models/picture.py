from sqlalchemy.orm import relationship

from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey


class Picture(Base):
    __tablename__ = "picture"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(200), nullable=False)
    created = Column(TIMESTAMP, nullable=False)
    owner = Column(Integer, ForeignKey('user.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship("Item", back_populates="pictures")

