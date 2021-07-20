from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


class Post(BaseModel):
    author_id: int
    created: datetime
    title: str
    body: str


class UserListModel(BaseModel):
    id: int
    name: str
    email: EmailStr
    posts: List[Post] = []


class UserRegisterModel(BaseModel):
    name: str
    email: EmailStr
