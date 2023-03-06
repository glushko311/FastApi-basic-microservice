from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey


class Stratigraphy(Base):
    __tablename__ = "stratigraphy"
    id = Column(Integer, primary_key=True, index=True)
    era = Column(String(100), nullable=False)
    period = Column(String(2000), nullable=True)
    epoch = Column(String(2000), nullable=True)
    age = Column(String(2000), nullable=True)
