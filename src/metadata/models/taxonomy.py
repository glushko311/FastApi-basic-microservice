from src.database import Base
from sqlalchemy import Column, Integer, String


class Taxonomy(Base):
    __tablename__ = "taxonomy"
    id = Column(Integer, primary_key=True, index=True)
    biological_phylum = Column(String(50), nullable=False, unique=False)
    biological_class = Column(String(50), nullable=True, unique=False)