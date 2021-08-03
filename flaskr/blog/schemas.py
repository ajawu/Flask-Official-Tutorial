from pydantic import BaseModel, EmailStr
import datetime
from flaskr.auth.schemas import UserDetailsSchema


class ContactSchema(BaseModel):
    name: str
    email: EmailStr
    message: str


class PostSchema(BaseModel):
    title: str
    body: str


class IdQuerySchema(BaseModel):
    id: int
