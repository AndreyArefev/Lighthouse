from datetime import datetime
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, Field

from ..Auth.schemas import SBaseInfoUser


class CategoryCreate(BaseModel):
    name_category: str = Field(min_length=2, max_length=100)


class Category(CategoryCreate):
    id_category: int

    class Config:
        orm_mode = True


class Tag(BaseModel):
    name_tag: str = Field(min_length=2, max_length=150)

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    name_event: str = Field(min_length=3, max_length=200)
    category: CategoryCreate
    tags: Optional[List[Tag]]
    time_event: datetime
    place_event: str
    about_event: str
    price: int
    age_limit: Optional[int]
    image: Optional[AnyHttpUrl]
    link: Optional[AnyHttpUrl]


class Event(EventCreate):
    id_event: int
    category: Category
    organizer: SBaseInfoUser





    class Config:
        orm_mode = True
