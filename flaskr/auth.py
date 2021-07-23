import functools
from flaskr.db import db_session
from flaskr.schemas import UserRegisterSchema, UserLoginSchema, UserListSchema
from flaskr.models import UserModel
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_pydantic import validate
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
@validate()
def register(body: UserRegisterSchema):
    if request.method == 'POST':
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


@bp.route('/login', methods=('GET', 'POST'))
@validate()
def login(body: UserLoginSchema):
    if request.method == 'POST':
        existing_user = UserListSchema.from_orm(
            db_session.query(UserModel.id, UserModel.email, UserModel.first_name, UserModel.last_name,
                             UserModel.is_admin, UserModel.is_verified, UserModel.password)
            .filter_by(email=body.email, is_active=True).first()
        )
        if existing_user:
            if check_password_hash(existing_user.password, body.password):
                session.clear()
                session['user'] = str(existing_user.json())
                return redirect(url_for('index'))

        flash('Invalid username or password')
    return render_template('auth/login.html')
