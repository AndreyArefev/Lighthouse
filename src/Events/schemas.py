from pydantic import BaseModel, AnyHttpUrl, Field
from typing import List, Optional
from datetime import datetime
from ..Auth.schemas import User


class Category(BaseModel):
    name_category: str
    #если жестко зашить категории, то делать Enum-класс доплнительно, для лучшей валидации,
    #но я думаю что нужна возможность админу добавлять категории, просто на фронте
    # не давать возможности вводить левые категории.


class Tag(BaseModel):
    name_tag: str


class Event(BaseModel):
    name_event: str = Field(min_length=3, max_length=200)
    category: List[Category]
    tags: List[Tag]
    time_event: datetime
    place_event: str
    about_event: str
    price: int
    age_limit: Optional[int]
    image: Optional[List[AnyHttpUrl]]
    link: Optional[AnyHttpUrl]
    organizer: User
