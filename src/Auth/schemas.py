from pydantic import BaseModel, EmailStr, AnyHttpUrl, constr, Field
from typing import List, Optional
from datetime import date


class BaseUser(BaseModel):
    username: str = Field(min_length=2, max_length=100)


class UpdateUser(BaseModel):
    password: str
    phone: constr(strip_whitespace=True,
                  regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$")
    image: Optional[AnyHttpUrl]


class CreateUser(BaseUser, UpdateUser):
    email: EmailStr


class GetUser(CreateUser):
    registered_at: date
    is_active: bool
    is_superuser: bool
    is_verified: bool




