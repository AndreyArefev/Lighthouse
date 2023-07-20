from datetime import date, timedelta
from typing import Optional

from pydantic import (AnyHttpUrl, BaseModel, BaseSettings, EmailStr, Field,
                      constr)


class SAuthUser(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=6, max_length=20)

class SBaseInfoUser(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: constr(strip_whitespace=True,
                  regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$")
    image: AnyHttpUrl

    class Config:
        orm_mode = True


class SGetUser(SBaseInfoUser):
    id: int
    registered_at: date
    is_active: bool
    is_verified: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class SCreateUser(SBaseInfoUser):
    password: str = Field(min_length=6, max_length=20)


class SUpdateUser(BaseModel):
    password: Optional[str]
    phone: Optional[constr(strip_whitespace=True,
                           regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$")]
    image: Optional[AnyHttpUrl]


