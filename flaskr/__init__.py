import os

from flask import Flask, jsonify
from pydantic import ValidationError


def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    upload_folder = 'flaskr/static/media/'

    app.config.from_mapping(
        SECRET_KEY='development',
        DATABASE=os.path.join(app.instance_path, 'flaskr.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.config['UPLOAD_FOLDER'] = upload_folder

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register commands
    from flaskr.db import init_db_command
    app.cli.add_command(init_db_command)

    # Register Blueprints
    from flaskr.auth.auth import auth_bp
    app.register_blueprint(auth_bp)

    from flaskr.blog.blog import blog_bp
    app.register_blueprint(blog_bp)

    # Error Handlers
    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_errors(e):
        return jsonify(e.errors())

    return app
