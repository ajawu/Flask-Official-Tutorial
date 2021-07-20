from flaskr import create_app
from flaskr.db import db_session

app = create_app()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.get('/')
def hello():
    return 'Hello World'
