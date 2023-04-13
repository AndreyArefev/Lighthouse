from pydantic import BaseModel, AnyHttpUrl, Field
from typing import List, Optional
from datetime import datetime
from ..Auth.schemas import UserRead, GetUser


class Category(BaseModel):
    name_category: str = Field(min_length=2, max_length=100)

    class Config:
        orm_mode = True


class Tag(BaseModel):
    name_tag: str = Field(min_length=2, max_length=150)

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    name_event: str = Field(min_length=3, max_length=200)
    category: Category
    tags: Optional[List[Tag]]
    time_event: datetime
    place_event: str
    about_event: str
    price: int
    age_limit: Optional[int]
    image: Optional[AnyHttpUrl]
    link: Optional[AnyHttpUrl]



class Event(BaseModel):
    name_event: str = Field(min_length=3, max_length=200)
    category: Category
    tags: Optional[List[Tag]]
    time_event: datetime
    place_event: str
    about_event: str
    price: int
    age_limit: Optional[int]
    image: Optional[AnyHttpUrl]
    link: Optional[AnyHttpUrl]
    organizer: UserRead



    class Config:
        orm_mode = True
