from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


api = Api()
db = SQLAlchemy()


def init_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')

    api.init_app(app)
    db.init_app(app)

    with app.app_context():
        from . import my_retail_api

        return app