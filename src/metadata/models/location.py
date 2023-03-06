from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, BOOLEAN


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)
    coordinates = Column(String(200), nullable=True)
    created = Column(TIMESTAMP, nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'))
    disabled = Column(BOOLEAN, nullable=False)
    # picture_id = Column(Integer, ForeignKey('picture.id'))
    # user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship("User", lazy="joined")