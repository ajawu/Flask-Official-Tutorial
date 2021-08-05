import functools

import ujson
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.auth import schemas
from flaskr.auth.models import UserModel
from flaskr.db import db_session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates', static_folder='static',
                    static_url_path='assets')


def register():
    if request.method == 'POST':
        body = schemas.UserRegisterSchema(**request.form)
        if db_session.query(UserModel.email == body.email).first():
            flash(f'User with email {body.email} is already registered.')
        else:
            new_user = UserModel(email=body.email,
                                 password=generate_password_hash(body.password),
                                 first_name=body.first_name.title(),
                                 last_name=body.last_name.title())
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


def login():
    if request.method == 'POST':
        body = schemas.UserLoginSchema(**request.form)
        existing_user = schemas.UserListSchema.from_orm(
            db_session.query(UserModel).filter_by(email=body.email, is_active=True).first()
        )
        if existing_user:
            if check_password_hash(existing_user.password, body.password):
                session.clear()
                del existing_user.password
                session['user'] = existing_user.json()
                return redirect(url_for('blog.home'))

        flash('Invalid username or password')
    return render_template('auth/login.html')


def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def edit_profile():
    if request.method == 'POST':
        form_data = schemas.UserEditSchema(**request.form)
        user_id = ujson.loads(session.get('user', '{}')).get('id', None)
        if user_id:
            db_session.query(UserModel).filter(UserModel.id == user_id).update({
                'first_name': form_data.first_name,
                'last_name': form_data.last_name,
                'email': form_data.email,
            })
            db_session.commit()
            updated_user = schemas.UserListSchema.from_orm(db_session.query(UserModel).
                                                           filter(UserModel.id == user_id).first())
            del updated_user.password
            session['user'] = updated_user.json()
            return redirect(url_for('auth.account_settings'))


def edit_password():
    if request.method == 'POST':
        user_id = ujson.loads(session.get('user', '{}')).get('id', None)
        body = schemas.PasswordChangeSchema(**request.form)
        old_password = db_session.query(UserModel.password).filter_by(id=user_id).first()

        if check_password_hash(old_password[0], body.old_password):
            if body.new_password == body.new_password_again:
                new_password = generate_password_hash(body.new_password)
                db_session.query(UserModel).filter(UserModel.id == user_id).update({
                    'password': new_password
                })
                db_session.commit()
                flash('Password updated successfully')
                return redirect(url_for('auth.account_settings'))
        else:
            flash('Enter valid current password')
            return redirect(url_for('auth.account_settings'))


def account_settings():
    return render_template('auth/profile_edit.html')


@auth_bp.before_app_request
def logged_in_user():
    if '/static/' not in request.path:
        user = session.get('user')
        if user is None:
            g.user = None
        else:
            user_obj = ujson.loads(user)
            g.user = user_obj


def login_required(view):
    functools.wraps(view)

    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view


def already_authenticated(view):
    functools.wraps(view)

    def wrapped_view(**kwargs):
        if g.user:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
