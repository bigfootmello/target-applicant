from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.flaskenv'))


# Set Environment Variables based on environment
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = environ.get("SQLALCHEMY_ECHO")


class ProdConfig(Config):
    FLASK_ENV = "production"
    FLASK_DEBUG = False 
    SQLALCHEMY_DATABASE_URI = environ.get('sqlite:///PROD_RETAIL.db')
    SQLALCHEMY_ECHO = False
    