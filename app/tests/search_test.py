from app.tests.base_test import BaseTest
from app.db import db
from app.models import User, Book, Lending, Reservation

import app.search as se


class SearchTest(BaseTest):
    def setUp(self):
        super(SearchTest, self).setUp()
        # Set up additional testing data
        with self.app_context():
            db.session.add(User(username='Test Lender 2', password='password', lender=True, borrower=False))
            db.session.add(Book(title='Test Novel', author='Test Author', year=2020, owner_id=1))
            db.session.add(Book(title='Test Poetry', author='Test Poet', year=2020, owner_id=3))
            db.session.add(Lending(book_id=1, user_id=2))
            db.session.add(Reservation(book_id=2, user_id=2))
            db.session.commit()

    def test_by_title(self):
        with self.app_context():
            result = se.by_title(None, 'Test Book').all()
            expected = Book.query.filter_by(title='Test Book').all()
            self.assertEqual(result, expected, 'Returned unexpected result')

    def test_by_author(self):
        with self.app_context():
            result = se.by_author(None, 'Test Author').all()
            expected = Book.query.filter_by(author='Test Author').all()
            self.assertEqual(result, expected, 'Returned unexpected result')

    def test_by_year(self):
        with self.app_context():
            result = se.by_year(None, 2020).all()
            expected = Book.query.filter_by(year=2020).all()
            self.assertEqual(result, expected, 'Returned unexpected result')

    def test_books_owned_by_me(self):
        with self.app_context():
            result = se.by_filter(None, 'owned_by_me', 1).all()
            expected = Book.query.filter_by(owner_id=1).all()
            self.assertEqual(result, expected, 'Returned unexpected result')

    def test_books_borrowed_by_me(self):
        with self.app_context():
            result = se.by_filter(None, 'borrowed_by_me', 2).all()
            expected = Book.query.filter_by(id=1).all()
            self.assertEqual(result, expected, 'Returned unexpected result')

    def test_books_reserved_by_me(self):
        with self.app_context():
            result = se.by_filter(None, 'reserved_by_me', 2).all()
            expected = Book.query.filter_by(id=2).all()
            self.assertEqual(result, expected, 'Returned unexpected result')
