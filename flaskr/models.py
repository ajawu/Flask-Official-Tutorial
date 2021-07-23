from flaskr.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    user_posts = relationship('PostModel')

    def __init__(self, email=None, password=None, first_name=None, last_name=None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'<User {self.name!r}>'


class PostModel(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    title = Column(String(150), nullable=False)
    body = Column(Text, nullable=False)

    def __init__(self, author_id=None, created=None, title=None, body=None):
        self.author_id = author_id
        self.created = created
        self.title = title
        self.body = body

    def __repr__(self):
        return f'<Post {self.title!r}>'
