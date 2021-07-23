from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


class PostSchema(BaseModel):
    author_id: int
    created: datetime
    title: str
    body: str


class UserListSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool
    is_verified: bool
    password: str

    class Config:
        orm_mode = True


class UserRegisterSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
