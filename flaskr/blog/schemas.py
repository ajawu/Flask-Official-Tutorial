from pydantic import BaseModel, EmailStr


class ContactSchema(BaseModel):
    name: str
    email: EmailStr
    message: str


class PostSchema(BaseModel):
    title: str
    ckeditor: str


class IdQuerySchema(BaseModel):
    id: int


class CommentSchema(BaseModel):
    name: str
    email: EmailStr
    comment: str
    post_id: int
