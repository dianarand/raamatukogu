from app.tests.base_test import BaseTest
from app.models import User, Book
from app.utils import save_to_db

import json


class AuthorisationTest(BaseTest):
    def test_register_user(self):
        with self.app() as a:
            with self.app_context():
                response = a.post('/register',
                                  data=json.dumps(
                                      {'username': 'lender', 'password': 'pass', 'role': 'lender'}),
                                  headers={'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(User.query.filter_by(username='lender'))
                self.assertDictEqual(json.loads(response.data), {'message': 'user created successfully'})

    def test_register_and_login(self):
        with self.app() as a:
            with self.app_context():
                a.post('/register',
                       data=json.dumps({'username': 'lender', 'password': 'pass', 'role': 'lender'}),
                       headers={'Content-Type': 'application/json'})
                response = a.post('/login',
                                  data=json.dumps({'username': 'lender', 'password':'pass'}),
                                  headers={'Content-Type': 'application/json'})
                self.assertIn('access_token', json.loads(response.data).keys())

    def test_register_duplicate(self):
        with self.app() as a:
            with self.app_context():
                a.post('/register',
                       data=json.dumps({'username': 'lender', 'password': 'pass', 'role': 'lender'}),
                       headers={'Content-Type': 'application/json'})
                response = a.post('/register',
                                  data=json.dumps(
                                      {'username': 'lender', 'password': 'pass', 'role': 'lender'}),
                                  headers={'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data), {'message': 'username already in use'})


class RoutesTest(BaseTest):
    def setUp(self):
        super(RoutesTest, self).setUp()
        with self.app() as a:
            with self.app_context():
                # Create users with proper passwords for testing
                a.post('/register',
                       data=json.dumps({'username': 'lender', 'password': 'pass', 'role': 'lender'}),
                       headers={'Content-Type': 'application/json'})
                a.post('/register',
                       data=json.dumps({'username': 'borrower', 'password': 'pass2', 'role': 'borrower'}),
                       headers={'Content-Type': 'application/json'})

    def test_add_book(self):
        with self.app() as a:
            with self.app_context():
                valid_data = json.dumps({'title': 'Test Book', 'author': 'Test Author', 'year': 2021})
                invalid_data = json.dumps({'title': 'Test Book'})

                # Attempt to add book as a borrower
                auth_request = a.post('/login',
                                      data=json.dumps({'username': 'borrower', 'password': 'pass2'}),
                                      headers={'Content-Type': 'application/json'})
                auth_header = f"JWT {json.loads(auth_request.data)['access_token']}"
                response = a.post('/books',
                                  data=valid_data,
                                  headers={'Authorization': auth_header,
                                           'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(json.loads(response.data), {'message': 'unauthorized'})

                # Attempt to add book with missing information
                auth_request2 = a.post('/login',
                                       data=json.dumps({'username': 'lender', 'password': 'pass'}),
                                       headers={'Content-Type': 'application/json'})
                auth_header2 = f"JWT {json.loads(auth_request2.data)['access_token']}"
                response2 = a.post('/books',
                                   data=invalid_data,
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response2.status_code, 400)
                self.assertDictEqual(json.loads(response2.data), {'message': 'invalid data posted'})

                # Add a book
                response3 = a.post('/books',
                                   data=valid_data,
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response3.status_code, 201)
                self.assertDictEqual(json.loads(response3.data), {'message': 'book added successfully'})

    def test_get_book(self):
        with self.app() as a:
            with self.app_context():
                auth_request = a.post('/login',
                                      data=json.dumps({'username': 'borrower', 'password': 'pass2'}),
                                      headers={'Content-Type': 'application/json'})
                auth_header = f"JWT {json.loads(auth_request.data)['access_token']}"

                # Attempt to get a non-existent book
                response = a.get('/book/10',
                                 headers={'Authorization': auth_header,
                                          'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'book not found'})

                # Get a book
                response = a.get('/book/1',
                                 headers={'Authorization': auth_header,
                                          'Content-Type': 'application/json'})
                expected = {
                    'id': 1,
                    'title': 'Test Book',
                    'author': 'Test Author',
                    'year': 2021,
                    'owner': 'Test Lender',
                    'active': True
                }
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)
                pass

    def test_remove_book(self):
        with self.app() as a:
            with self.app_context():
                # Attempt to remove a book as a borrower
                auth_request = a.post('/login',
                                      data=json.dumps({'username': 'borrower', 'password': 'pass2'}),
                                      headers={'Content-Type': 'application/json'})
                auth_header = f"JWT {json.loads(auth_request.data)['access_token']}"
                response = a.delete('/book/1',
                                    headers={'Authorization': auth_header,
                                             'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(json.loads(response.data), {'message': 'unauthorized'})

                # Attempt to remove a non-existent book
                auth_request2 = a.post('/login',
                                       data=json.dumps({'username': 'lender', 'password': 'pass'}),
                                       headers={'Content-Type': 'application/json'})
                auth_header2 = f"JWT {json.loads(auth_request2.data)['access_token']}"
                response2 = a.delete('/book/10',
                                     headers={'Authorization': auth_header2,
                                              'Content-Type': 'application/json'})
                self.assertEqual(response2.status_code, 404)
                self.assertDictEqual(json.loads(response2.data), {'message': 'book not found'})

                # Attempt to remove a book owned by another user
                response3 = a.delete('/book/1',
                                     headers={'Authorization': auth_header2,
                                              'Content-Type': 'application/json'})
                self.assertEqual(response3.status_code, 401)
                self.assertDictEqual(json.loads(response3.data), {'message': 'unauthorized'})

                # Remove a book
                save_to_db(Book(title='Test Book', author='Test Author', year=2021, owner_id=3))
                response4 = a.delete('/book/2',
                                     headers={'Authorization': auth_header2,
                                              'Content-Type': 'application/json'})
                self.assertEqual(response4.status_code, 200)
                self.assertDictEqual(json.loads(response4.data), {'message': 'book successfully removed'})

                # Attempt to remove an already removed book
                response5 = a.delete('/book/2',
                                     headers={'Authorization': auth_header2,
                                              'Content-Type': 'application/json'})
                self.assertEqual(response5.status_code, 400)
                self.assertDictEqual(json.loads(response5.data), {'message': 'book already removed'})
                pass

    def test_lend_book(self):
        with self.app() as a:
            with self.app_context():
                # Attempt to lend a book as a borrower
                # Attempt to lend a book without providing a borrower
                # Attempt to lend a book to a non-existent borrower
                # Attempt to lend a book owned by another user
                # Attempt to lend a non-existent book
                # Lend a book
                # Attempt to lend a book that is already lent
                pass

    def test_borrow_book(self):
        with self.app() as a:
            with self.app_context():
                # Attempt to borrow a book as a lender
                # Attempt to borrow a non-existent book
                # Borrow a book
                # Attempt to borrow a book that is already borrowed
                pass

    def test_return_book(self):
        with self.app() as a:
            with self.app_context():
                # Attempt to return a book that is not borrowed
                # Attempt to return a book that is borrowed by someone else
                # Attempt to return a book that is owned by someone else
                # Attempt to return a non-existent book
                # Return a book
                # Attempt to return a book that is already returned
                pass

    def test_reserve_book(self):
        with self.app() as a:
            with self.app_context():
                # Attempt to reserve a book as a lender
                # Attempt to reserve a non-existent book
                # Reserve a book
                # Attempt to reserve a book that is already reserved
                pass

    def test_cancel_reservation(self):
        with self.app() as a:
            with self.app_context():
                # Attempt to cancel a reservation on a book that is not reserved
                # Attempt to cancel a reservation on a book that is reserved by someone else
                # Attempt cancel a reservation on a book that is owned by someone else
                # Attempt to reserve a non-existent book
                # Reserve a book
                # Attempt to reserve book that is already reserved
                pass

    def test_remove_book(self):
        with self.app() as a:
            with self.app_context():
                # Attempt to remove book as a borrower
                # Attempt to remove a book owned by someone else
                # Attempt to remove a non-existent book
                # Remove a book
                # Attempt to remove a book that is already removed
                pass
