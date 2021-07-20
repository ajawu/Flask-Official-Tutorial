from flaskr.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    posts = relationship('posts')

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'


class PostModel(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
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
