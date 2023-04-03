from pydantic import BaseModel, EmailStr, AnyHttpUrl, constr
from typing import List
from datetime import date


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: constr(strip_whitespace=True,
                  regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$")
    image: AnyHttpUrl



