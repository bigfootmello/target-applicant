from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


api = Api()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///DEV_RETAIL.db"
    app.config['SQLALCHEMY_ECHO'] = True

    api.init_app(app)
    db.init_app(app)

    with app.app_context():
        from . import my_retail_api

        db.create_all()

        return app