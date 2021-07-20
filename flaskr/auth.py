import functools
from flaskr.pydantic_models import UserRegisterModel
from flaskr.models import UserModel
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register_new_user():
    if request.method == 'POST':
        user = UserRegisterModel(**request.form)
        existing_user = UserModel()
