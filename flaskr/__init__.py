import os

from flask import Flask, jsonify
from pydantic import ValidationError


def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register commands
    from flaskr.auth.db import init_db_command
    app.cli.add_command(init_db_command)

    # Register Blueprints
    from flaskr.auth.auth import bp
    app.register_blueprint(bp)

    # Error Handlers
    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_errors(e):
        return jsonify(e.errors())

    return app
