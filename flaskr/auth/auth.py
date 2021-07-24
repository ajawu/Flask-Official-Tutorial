import functools

from flaskr.auth.db import db_session
from flaskr.auth import schemas
from flaskr.auth.models import UserModel
import ujson
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates', static_folder='static',
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
            db_session.query(UserModel.id, UserModel.email, UserModel.first_name, UserModel.last_name,
                             UserModel.is_admin, UserModel.is_verified, UserModel.password)
            .filter_by(email=body.email, is_active=True).first()
        )
        if existing_user:
            if check_password_hash(existing_user.password, body.password):
                session.clear()
                session['user'] = ujson.dumps(existing_user.json())
                return redirect(url_for('index'))

        flash('Invalid username or password')
    return render_template('auth/login.html')


def logout():
    session.clear()
    return redirect('auth.login')


def change_password():
    if request.method == 'POST':
        body = schemas.PasswordChangeSchema(**request.form)


@bp.before_app_request
def logged_in_user():
    user = session.get('user')
    if user is None:
        g.user = None
    else:
        g.user = ujson.loads(user)


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
