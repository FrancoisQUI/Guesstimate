from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    class Config:
        from_attributes = True

class CardBase(BaseModel):
    name: str
    image_url: Optional[str] = None
    wiki_link: Optional[str] = None
    attributes: Dict[str, Any]

class CardCreate(CardBase):
    tag_names: List[str] = []

class Card(CardBase):
    id: int
    tags: List[Tag] = []
    class Config:
        from_attributes = True
