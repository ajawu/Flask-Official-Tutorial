from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


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


class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str
    new_password_again: str


class UserDetailsSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
