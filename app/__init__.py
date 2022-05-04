"""A simple flask web app"""
import os
from flask import Flask, render_template
from app.cli import create_database
from app.db import db, database
from app.db.models import User
import flask_login
from flask_bootstrap import Bootstrap5

from app.simple_pages import simple_pages
from app.recipes import recipes
from app.auth import auth
from app.context_processors import utility_text_processors

login_manager = flask_login.LoginManager()


def page_not_found(e):
    return render_template("404.html"), 404


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app = Flask(__name__)
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    # app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'
    bootstrap = Bootstrap5(app)
    app.context_processor(utility_text_processors)
    app.register_error_handler(404, page_not_found)
    # db_dir = "database/db.sqlite"
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(simple_pages)
    app.register_blueprint(database)
    app.register_blueprint(auth)
    app.register_blueprint(recipes)
    db.init_app(app)

    # add command function to cli commands
    app.cli.add_command(create_database)
    return app


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None