from app.tests.base_test import BaseTest
from app.models import User, Book, Lending, Reservation
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
                self.assertDictEqual(json.loads(response.data), {'message': 'Kasutaja loodud edukalt'})

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
                self.assertDictEqual(json.loads(response.data), {'message': 'Kasutajanimi juba kasutuses'})


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
                self.assertDictEqual(json.loads(response.data), {'message': 'Puuduvad õigused'})

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
                self.assertDictEqual(json.loads(response2.data), {'message': 'Puudulikud andmed'})

                # Add a book
                response3 = a.post('/books',
                                   data=valid_data,
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response3.status_code, 201)
                self.assertDictEqual(json.loads(response3.data), {'message': 'Raamat lisatud edukalt', 'id': 2})

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
                self.assertDictEqual(json.loads(response.data), {'message': 'Raamatut ei leitud'})

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
                    'active': True,
                    'lending': None,
                    'deadline': None,
                    'overtime': False,
                    'reservation': None
                }
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

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
                self.assertDictEqual(json.loads(response.data), {'message': 'Puuduvad õigused'})

                # Attempt to remove a non-existent book
                auth_request2 = a.post('/login',
                                       data=json.dumps({'username': 'lender', 'password': 'pass'}),
                                       headers={'Content-Type': 'application/json'})
                auth_header2 = f"JWT {json.loads(auth_request2.data)['access_token']}"
                response2 = a.delete('/book/10',
                                     headers={'Authorization': auth_header2,
                                              'Content-Type': 'application/json'})
                self.assertEqual(response2.status_code, 404)
                self.assertDictEqual(json.loads(response2.data), {'message': 'Raamatut ei leitud'})

                # Attempt to remove a book owned by another user
                response3 = a.delete('/book/1',
                                     headers={'Authorization': auth_header2,
                                              'Content-Type': 'application/json'})
                self.assertEqual(response3.status_code, 401)
                self.assertDictEqual(json.loads(response3.data), {'message': 'Puuduvad õigused'})

                # Remove a book
                save_to_db(Book(title='Test Book', author='Test Author', year=2021, owner_id=3))
                response4 = a.delete('/book/2',
                                     headers={'Authorization': auth_header2,
                                              'Content-Type': 'application/json'})
                self.assertEqual(response4.status_code, 200)
                self.assertDictEqual(json.loads(response4.data), {'message': 'Raamat eemaldatud edukalt'})

                # Attempt to remove an already removed book
                response5 = a.delete('/book/2',
                                     headers={'Authorization': auth_header2,
                                              'Content-Type': 'application/json'})
                self.assertEqual(response5.status_code, 400)
                self.assertDictEqual(json.loads(response5.data), {'message': 'Raamatut juba eemaldatud'})

    def test_lend_book(self):
        with self.app() as a:
            with self.app_context():
                save_to_db(Book(title='Test Book', author='Test Author', year=2021, owner_id=3))
                valid_data = json.dumps({'borrower': 'borrower'})
                invalid_data = json.dumps({'user_id': 4})
                invalid_data2 = json.dumps({'borrower': 'borrower2'})

                # Attempt to lend a book as a borrower
                auth_request = a.post('/login',
                                      data=json.dumps({'username': 'borrower', 'password': 'pass2'}),
                                      headers={'Content-Type': 'application/json'})
                auth_header = f"JWT {json.loads(auth_request.data)['access_token']}"
                response = a.post('/book/2/lend',
                                  data=valid_data,
                                  headers={'Authorization': auth_header,
                                           'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(json.loads(response.data), {'message': 'Puuduvad õigused'})

                # Attempt to lend a book without providing a borrower
                auth_request2 = a.post('/login',
                                       data=json.dumps({'username': 'lender', 'password': 'pass'}),
                                       headers={'Content-Type': 'application/json'})
                auth_header2 = f"JWT {json.loads(auth_request2.data)['access_token']}"
                response2 = a.post('/book/2/lend',
                                   data=invalid_data,
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response2.status_code, 400)
                self.assertDictEqual(json.loads(response2.data), {'message': 'invalid data'})

                # Attempt to lend a book to a non-existent borrower
                response3 = a.post('/book/2/lend',
                                   data=invalid_data2,
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response3.status_code, 404)
                self.assertDictEqual(json.loads(response3.data), {'message': 'Kasutajat ei leitud'})

                # Attempt to lend a book owned by another user
                response4 = a.post('/book/1/lend',
                                   data=valid_data,
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response4.status_code, 404)
                self.assertDictEqual(json.loads(response4.data), {'message': 'Raamatut ei leitud'})

                # Attempt to lend a non-existent book
                response5 = a.post('/book/10/lend',
                                   data=valid_data,
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response5.status_code, 404)
                self.assertDictEqual(json.loads(response4.data), {'message': 'Raamatut ei leitud'})

                # Lend a book
                response6 = a.post('/book/2/lend',
                                   data=valid_data,
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response6.status_code, 200)
                result = json.loads(response6.data)
                self.assertEqual(result['book'], 'Test Book')
                self.assertEqual(result['user'], 'borrower')

    def test_borrow_book(self):
        with self.app() as a:
            with self.app_context():
                save_to_db(Book(title='Test Book', author='Test Author', year=2021, owner_id=3))

                # Attempt to borrow a book as a lender
                auth_request = a.post('/login',
                                      data=json.dumps({'username': 'lender', 'password': 'pass'}),
                                      headers={'Content-Type': 'application/json'})
                auth_header = f"JWT {json.loads(auth_request.data)['access_token']}"
                response = a.post('/book/2/borrow',
                                  headers={'Authorization': auth_header,
                                           'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(json.loads(response.data), {'message': 'Puuduvad õigused'})

                # Attempt to borrow a non-existent book
                auth_request2 = a.post('/login',
                                       data=json.dumps({'username': 'borrower', 'password': 'pass2'}),
                                       headers={'Content-Type': 'application/json'})
                auth_header2 = f"JWT {json.loads(auth_request2.data)['access_token']}"
                response2 = a.post('/book/10/borrow',
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response2.status_code, 404)
                self.assertDictEqual(json.loads(response2.data), {'message': 'Raamatut ei leitud'})

                # Borrow a book
                response3 = a.post('/book/2/borrow',
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response3.status_code, 200)
                result = json.loads(response3.data)
                self.assertEqual(result['book'], 'Test Book')
                self.assertEqual(result['user'], 'borrower')

    def test_return_book(self):
        with self.app() as a:
            with self.app_context():
                save_to_db(Lending(book_id=1, user_id=1))
                save_to_db(Book(title='Test Book', author='Test Author', year=2021, owner_id=3))
                save_to_db(Lending(book_id=2, user_id=4))
                auth_request = a.post('/login',
                                      data=json.dumps({'username': 'borrower', 'password': 'pass2'}),
                                      headers={'Content-Type': 'application/json'})
                auth_header = f"JWT {json.loads(auth_request.data)['access_token']}"

                # Attempt to return a book that is borrowed by someone else
                response = a.post('/book/1/return',
                                  headers={'Authorization': auth_header,
                                           'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(json.loads(response.data), {'message': 'Puuduvad õigused'})

                # Attempt to return a non-existent book
                response2 = a.post('/book/10/return',
                                   headers={'Authorization': auth_header,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response2.status_code, 404)
                self.assertDictEqual(json.loads(response2.data), {'message': 'Raamatut ei leitud'})

                # Return a book
                response3 = a.post('/book/2/return',
                                   headers={'Authorization': auth_header,
                                            'Content-Type': 'application/json'})
                result = json.loads(response3.data)
                self.assertEqual(response3.status_code, 200)
                self.assertEqual(result, {'message': 'Raamat on nüüd saadaval'})

    def test_reserve_book(self):
        with self.app() as a:
            with self.app_context():
                # Attempt to reserve a book as a lender
                auth_request = a.post('/login',
                                      data=json.dumps({'username': 'lender', 'password': 'pass'}),
                                      headers={'Content-Type': 'application/json'})
                auth_header = f"JWT {json.loads(auth_request.data)['access_token']}"
                response = a.post('/book/1/reserve',
                                  headers={'Authorization': auth_header,
                                           'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(json.loads(response.data), {'message': 'Puuduvad õigused'})

                # Attempt to reserve a non-existent book
                auth_request2 = a.post('/login',
                                       data=json.dumps({'username': 'borrower', 'password': 'pass2'}),
                                       headers={'Content-Type': 'application/json'})
                auth_header2 = f"JWT {json.loads(auth_request2.data)['access_token']}"
                response2 = a.post('/book/10/reserve',
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                self.assertEqual(response2.status_code, 404)
                self.assertDictEqual(json.loads(response2.data), {'message': 'Raamatut ei leitud'})

                # Reserve a book
                response3 = a.post('/book/1/reserve',
                                   headers={'Authorization': auth_header2,
                                            'Content-Type': 'application/json'})
                result = json.loads(response3.data)
                self.assertEqual(response3.status_code, 200)
                self.assertEqual(result['book'], 'Test Book')
                self.assertEqual(result['user'], 'borrower')

    def test_cancel_reservation(self):
        with self.app() as a:
            with self.app_context():
                auth_request = a.post('/login',
                                      data=json.dumps({'username': 'borrower', 'password': 'pass2'}),
                                      headers={'Content-Type': 'application/json'})
                auth_header = f"JWT {json.loads(auth_request.data)['access_token']}"

                # Attempt to cancel a reservation for a non-existent book
                response = a.post('/book/10/cancel',
                                  headers={'Authorization': auth_header,
                                           'Content-Type': 'application/json'})
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'Raamatut ei leitud'})

                # Cancel a reservation
                save_to_db(Reservation(book_id=1, user_id=4))
                response2 = a.post('/book/1/cancel',
                                   headers={'Authorization': auth_header,
                                            'Content-Type': 'application/json'})
                result = json.loads(response2.data)
                self.assertEqual(response2.status_code, 200)
                self.assertEqual(result, {'message': 'Raamat on nüüd saadaval'})
