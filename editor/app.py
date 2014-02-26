#!/usr/bin/env python
from flask import Flask
from flask.ext.mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore
from editor.models import db, User, Role


def create_app():
    app = Flask("editor")
    app.config.from_object('editor.config.general')
    app.config.from_object('editor.config.email')
    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run...
        db.create_all()

    return app

# Create app
app = create_app()

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Setup mail extension
mail = Mail(app)

# initialize views
from editor import views, models
