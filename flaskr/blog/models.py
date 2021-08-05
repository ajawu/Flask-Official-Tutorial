from flaskr.db import Base
from sqlalchemy import Table, Column, String, Integer, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from slugify import slugify


class ContactModel(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text(length=50), nullable=False)
    email = Column(String, nullable=False)
    message = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    def __repr__(self):
        return f'<Contact - {self.name} {self.email}>'


association_table = Table('association', Base.metadata,
                          Column('post_id', ForeignKey('post.id'), primary_key=True),
                          Column('category_id', ForeignKey('category.id'), primary_key=True))


class PostModel(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    title = Column(String(150), nullable=False)
    hero_image_url = Column(String, nullable=True)
    list_image_url = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    comments = relationship('CommentModel')
    categories = relationship(
        "CategoryModel",
        secondary=association_table,
        back_populates="posts"
    )

    def __init__(self, author_id=None, created=None, title=None, body=None, hero_image_url=None, list_image_url=None):
        self.author_id = author_id
        self.created = created
        self.title = title
        self.body = body
        self.hero_image_url = hero_image_url
        self.list_image_url = list_image_url

    def __repr__(self):
        return f'<Post - {self.title!r}>'


class CategoryModel(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    posts = relationship(
        "PostModel",
        secondary=association_table,
        back_populates="categories"
    )

    def __init__(self, name):
        self.name = name
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Category - {self.slug}>'


class CommentModel(Base):
    __tablename__ = 'comment'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    comment = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    def __init__(self, name, email, comment, post_id):
        self.name = name
        self.email = email
        self.comment = comment
        self.post_id = post_id
