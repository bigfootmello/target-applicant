from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.flaskenv'))


# Set Environment Variables based on environment
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///DEV_RETAIL.db"
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///PROD_RETAIL.db'
    SQLALCHEMY_ECHO = False
    