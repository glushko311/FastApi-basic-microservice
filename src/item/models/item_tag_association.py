from src.database import Base
from sqlalchemy import Column, ForeignKey


class ItemTagAssociation(Base):
    __tablename__ = "item_tag_association"
    item_id = Column(ForeignKey("item.id"), primary_key=True)
    tag_id = Column(ForeignKey("tag.id"), primary_key=True)
