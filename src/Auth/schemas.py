from pydantic import BaseModel, EmailStr, AnyHttpUrl, constr, Field
from typing import List, Optional
from datetime import date
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str = Field(min_length=2, max_length=100)
    registered_at: date
    phone: constr(strip_whitespace=True,
                  regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$")
    image: AnyHttpUrl

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(min_length=2, max_length=100)
    password: str
    phone: constr(strip_whitespace=True,
                  regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$")
    image: Optional[AnyHttpUrl]


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str]
    phone: Optional[constr(strip_whitespace=True,
                           regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$")]
    image: Optional[AnyHttpUrl]


class GetUser(BaseModel):
    username: str = Field(min_length=2, max_length=100)