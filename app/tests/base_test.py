from unittest import TestCase
from app import app
from app.db import db
from app.models import Book, User


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        # Create a database
        with app.app_context():
            db.create_all()
        # Create a test client
        self.app = app.test_client
        self.app_context = app.app_context
        # Initialise some test data
        with app.app_context():
            db.session.add(
                User(
                    username='Test Lender',
                    password='password',
                    lender=True,
                    borrower=False
                )
            )
            db.session.add(
                User(
                    username='Test Borrower',
                    password='password',
                    lender=False,
                    borrower=True
                )
            )
            db.session.add(
                Book(
                    title='Test Book',
                    author='Test Author',
                    year=2021,
                    owner_id=1,
                )
            )
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
