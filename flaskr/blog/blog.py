import os
import uuid
from datetime import datetime

import ujson
from flask import (
    Blueprint, flash, g, render_template, request, session, redirect, url_for, abort, current_app
)
from werkzeug.utils import secure_filename

from flaskr.auth import models as auth_models, decorators
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
    return render_template('blog/index.html', posts=posts)


@decorators.login_required
def post_create():
    """Create new post"""
    g.page = 'post_create'
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
                body=post_object.ckeditor,
            )
            post.categories = post_categories
            db_session.add(post)
            db_session.commit()
            return redirect(url_for('blog.post_details', post_id=post.id))

    elif request.method == 'GET':
        categories = db_session.query(models.CategoryModel).all()
        return render_template('blog/post_create.html', categories=categories)


def post_details():
    """View Details of a post with matching post id"""
    post_id = schemas.IdQuerySchema(id=request.args.get('post_id')).id
    post_author = db_session.query(models.PostModel, auth_models.UserModel).join(auth_models.UserModel).filter(
        models.PostModel.id == post_id).first()
    if post_author:
        comments = db_session.query(models.CommentModel).filter_by(post_id=post_id).all()
        return render_template('blog/post_details.html', post=post_author[0], user=post_author[1], comments=comments)
    else:
        abort(404, 'Post with matching id not found')


@decorators.login_required
def post_update():
    """Update the details of post if user id matches post author id"""
    post_id = schemas.IdQuerySchema(id=request.args.get('post_id')).id
    if request.method == 'POST':
        post_object = schemas.PostSchema(**request.form)
        post = db_session.query(models.PostModel).filter_by(id=post_id).first()
        post_categories = [db_session.query(models.CategoryModel).filter_by(id=cat_id).first()
                           for cat_id in request.form.getlist('categories')]

        # Process post image uploads
        hero_image, list_image = request.files.get('hero-image-field'), request.files.get('list-image-field')
        if hero_image and list_image and utils.allowed_file([hero_image.filename, list_image.filename]):
            # Delete previous images
            try:
                os.remove(f'{current_app.config["UPLOAD_FOLDER"]}posts/{post.hero_image_url}')
            except OSError:
                pass
            try:
                os.remove(f'{current_app.config["UPLOAD_FOLDER"]}posts/{post.list_image_url}')
            except OSError:
                pass

            hero_image_filename = f'{uuid.uuid4().hex}.{list_image.filename.split(".")[-1]}'
            list_image_filename = f'{uuid.uuid4().hex}.{list_image.filename.split(".")[-1]}'
            hero_image.save(f'{current_app.config["UPLOAD_FOLDER"]}posts/{hero_image_filename}')
            list_image.save(f'{current_app.config["UPLOAD_FOLDER"]}posts/{list_image_filename}')

            db_session.query(models.PostModel).filter(models.PostModel.id == post_id).update({
                'title': post_object.title,
                'body': post_object.body,
                'list_image_url': list_image_filename,
                'hero_image_url': hero_image_filename,
            })
        else:
            db_session.query(models.PostModel).filter(models.PostModel.id == post_id).update({
                'title': post_object.title,
                'body': post_object.body,
            })
        post.categories = post_categories
        db_session.commit()
        return redirect(url_for('blog.post_details', post_id=post_id))
    elif request.method == 'GET':
        user_id = ujson.loads(session.get('user'))['id']
        post = db_session.query(models.PostModel).filter_by(id=post_id, author_id=user_id).first()
        categories = db_session.query(models.CategoryModel).all()
        if post:
            return render_template('blog/post_update.html', categories=categories, post=post)
        else:
            abort(404, 'Post with matching id not found')


@decorators.login_required
def post_delete():
    """Delete post if post author id matches logged in user id"""
    post_id = schemas.IdQuerySchema(id=request.form.get('post_id')).id
    user_id = ujson.loads(session.get('user', '{}')).get('id')
    db_session.query(models.PostModel).filter_by(id=post_id, author_id=user_id).delete()
    return redirect(url_for('blog.profile'))


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


def search_post():
    """Search for posts by name"""
    search_keyword = request.args.get('keyword')
    if search_keyword:
        matching_posts = db_session.query(models.PostModel, auth_models.UserModel).join(auth_models.UserModel)\
            .filter(models.PostModel.title.ilike(f'%{search_keyword}%')).all()
        return render_template('blog/search_result.html', posts=matching_posts, keyword=search_keyword)
    else:
        return redirect(url_for('blog.home'))


@decorators.login_required
def profile():
    """Details of current logged in user"""
    g.page = 'profile'
    author = ujson.loads(session.get('user'))
    posts = db_session.query(models.PostModel).filter_by(author_id=author['id']).all()
    return render_template('blog/profile.html', author=author, posts=posts)


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


def add_comment():
    """Add new comment to post"""
    comment_schema = schemas.CommentSchema(**request.form)
    comment = models.CommentModel(
        name=comment_schema.name,
        email=comment_schema.email,
        comment=comment_schema.comment,
        post_id=comment_schema.post_id
    )
    db_session.add(comment)
    db_session.commit()
    return redirect(url_for('blog.post_details', post_id=comment_schema.post_id))
