import os
import uuid
from datetime import datetime

import ujson
from flask import (
    Blueprint, flash, g, render_template, request, session, redirect, url_for, abort, current_app
)
from werkzeug.utils import secure_filename

from flaskr.auth import models as auth_models
from flaskr.blog import schemas, models
from flaskr.blog import utils
from flaskr.db import db_session

blog_bp = Blueprint('blog', __name__, url_prefix='/', template_folder='templates', static_folder='static',
                    static_url_path='assets')


@blog_bp.before_request
def load_categories():
    g.categories = db_session.query(models.CategoryModel).all()


def home():
    """List all posts for the blog home page"""
    g.page = 'home'
    posts = db_session.query(models.PostModel, auth_models.UserModel).join(auth_models.UserModel).all()
    post_categories = db_session.query(models.CategoryModel).all()
    return render_template('blog/index.html', posts=posts, categories=post_categories)


def post_create():
    """Create new post"""
    if request.method == 'POST':
        post_object = schemas.PostSchema(**request.form)
        # Process post image uploads
        if 'hero-image-field' not in request.files and 'list-image-field' not in request.files:
            flash('Post image missing')
            return redirect(request.url)
        hero_image, list_image = request.files['hero-image-field'], request.files['list-image-field']
        if hero_image.filename == '' or list_image.filename == 'list-image-field':
            flash('No selected file')
            return redirect(request.url)
        if hero_image and list_image and utils.allowed_file([hero_image.filename, list_image.filename]):
            hero_image_filename = f'{uuid.uuid4().hex}.{list_image.filename.split(".")[-1]}'
            list_image_file_name = f'{uuid.uuid4().hex}.{list_image.filename.split(".")[-1]}'
            hero_image.save(f'{current_app.config["UPLOAD_FOLDER"]}posts/{hero_image_filename}')
            list_image.save(f'{current_app.config["UPLOAD_FOLDER"]}posts/{list_image_file_name}')

            post_categories = [db_session.query(models.CategoryModel).filter_by(id=cat_id).first()
                               for cat_id in request.form.getlist('categories')]
            # Save Post
            post = models.PostModel(
                author_id=ujson.loads(session.get('user'))['id'],
                created=datetime.utcnow(),
                title=post_object.title,
                list_image_url=list_image_file_name,
                hero_image_url=hero_image_filename,
                body=post_object.body,
            )
            post.categories = post_categories
            db_session.add(post)
            db_session.commit()
            return redirect(url_for('blog.post_details', post_id=post.id))

    categories = db_session.query(models.CategoryModel).all()
    return render_template('blog/post_create.html', categories=categories, author_id=1)


def post_details():
    """View Details of a post with matching post id"""
    post_id = schemas.IdQuerySchema(id=request.args.get('post_id')).id
    post_author = db_session.query(models.PostModel, auth_models.UserModel).join(auth_models.UserModel).filter_by(
        id=post_id).first()
    return render_template('blog/post_details.html', post=post_author[0], user=post_author[1])


def post_update():
    """Update the details of post if user id matches post author id"""
    post_id = schemas.IdQuerySchema(id=request.args.get('post_id')).id
    if request.method == 'POST':
        pass
    return render_template('blog/contact.html')


def post_delete():
    """Delete post if post author id matches logged in user id"""
    post_id = schemas.IdQuerySchema(id=request.form.get('post_id')).id
    post = db_session.query(models.PostModel).filter_by(id=post_id)
    user_id = ujson.loads(session.get('user', '{}')).get('id')
    if post.author_id == user_id:
        db_session.query(models.PostModel).filter_by(id=post_id).delete()
    else:
        return redirect(url_for('blog.home'))
    return render_template('blog/contact.html')


def post_by_categories():
    """List posts in category with matching slug"""
    g.page = 'categories'
    category_slug = request.args.get('slug')
    # post_from_category = db_session.query(models.PostModel). \
    #     filter(models.PostModel.categories.any(models.CategoryModel.slug == category_slug)).all()
    post_from_category = db_session.query(models.PostModel, auth_models.UserModel).join(auth_models.UserModel). \
        filter(models.PostModel.categories.any(models.CategoryModel.slug == category_slug)).all()
    return render_template('blog/post_by_category.html', category_name=category_slug,
                           posts=post_from_category)


def me_details():
    """Details of current logged in user"""
    return render_template('blog/author_posts.html')


def contact():
    """Blog contact page"""
    g.page = 'contact'
    if request.method == 'POST':
        contact_body = schemas.ContactSchema(**request.form)
        new_contact = models.ContactModel(name=contact_body.name,
                                          email=contact_body.email,
                                          message=contact_body.message)
        db_session.add(new_contact)
        db_session.commit()
        flash('Message saved successfully')

    return render_template('blog/contact.html')


def author_details():
    """Author details page"""
    id_author = schemas.IdQuerySchema(id=request.args.get('author_id')).id
    author = db_session.query(auth_models.UserModel).filter_by(id=id_author).first()
    if author is not None:
        posts = db_session.query(models.PostModel).filter_by(author_id=id_author).all()
        return render_template('blog/author_posts.html', posts=posts, author=author)
    else:
        abort(404, 'Author with matching id not found')
