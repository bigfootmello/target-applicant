from flask_testing import TestCase
from my_retail import create_app
from my_retail.models import db


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///DEV_RETAIL.db"
        app.config['SQLALCHEMY_ECHO'] = True
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        return app

    def setUp(self):
        self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
