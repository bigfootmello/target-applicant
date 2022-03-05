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
    #SQLALCHEMY_DATABASE_URI = "sqlite:///DEV_RETAIL.db"
    SQLALCHEMY_DATABASE_URI = "postgresql://spbwjrwgaxozyd:498f4047086c77222827fd5e75ec3a78c129eb6a0c69dbca59a108e2647b8559@ec2-54-209-221-231.compute-1.amazonaws.com:5432/dftln3an6fc92k"
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///PROD_RETAIL.db'
    SQLALCHEMY_ECHO = False
    