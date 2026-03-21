from sqlalchemy import Column, Integer, String, JSON, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

card_tag_association = Table(
    'card_tag', Base.metadata,
    Column('card_id', Integer, ForeignKey('cards.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    cards = relationship("Card", secondary=card_tag_association, back_populates="tags")

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String, nullable=True)
    wiki_link = Column(String, nullable=True)
    attributes = Column(JSON) # e.g., {"poids": 12, "taille": 1.4}
    tags = relationship("Tag", secondary=card_tag_association, back_populates="cards")
