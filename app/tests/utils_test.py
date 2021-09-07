from app.tests.base_test import BaseTest
from app.models import Book, Lending, Reservation, User
import app.utils as ut

from datetime import date, timedelta


class UtilitiesTest(BaseTest):
    def test_checkout_and_print_usage(self):
        with self.app_context():
            book = Book.query.first()
            # Check out a book without a reservation
            expected = {
                'book': 'Test Book',
                'user': 'Test Borrower',
                'date_begin': date.today(),
                'date_end': None,
                'deadline': date.today() + timedelta(weeks=4)
            }
            self.assertDictEqual(ut.checkout(book, 2), expected,
                                 'Unable to check out a book or returned unexpected information')

            # Attempt to check out a book that is already checked out
            response = ut.checkout(book, 2)
            self.assertDictEqual(response[0], ut.unavailable_message,
                                 'Did not return correct message when attempted to check out an unavailable book')
            self.assertEqual(response[1], 400,
                             'Returned unexpected status code')

    def test_checkout_with_reservation(self):
        with self.app_context():
            book = Book.query.first()
            # Check out a book with a reservation
            ut.save_to_db(Reservation(book_id=1, user_id=2))
            expected = {
                'book': 'Test Book',
                'user': 'Test Borrower',
                'date_begin': date.today(),
                'date_end': None,
                'deadline': date.today() + timedelta(weeks=4)
            }
            self.assertDictEqual(ut.checkout(book, 2), expected,
                                 'Unable to check out a book with a reservation')

    def test_checkout_reserved(self):
        with self.app_context():
            book = Book.query.first()
            # Attempt to check out a book reserved by someone else
            ut.save_to_db(Reservation(book_id=1, user_id=1))
            response = ut.checkout(book, 2)
            self.assertDictEqual(response[0], ut.unavailable_message,
                                 'Did not return correct message when attempted to check out an unavailable book')
            self.assertEqual(response[1], 400,
                             'Returned unexpected status code')

    def test_checkout_inactive(self):
        with self.app_context():
            book = Book.query.first()
            # Attempt to check out an inactive book
            book.active = False
            ut.save_to_db(book)
            response = ut.checkout(book, 2)
            self.assertDictEqual(response[0], ut.unavailable_message,
                                 'Did not return correct message when attempted to check out an inactive book')
            self.assertEqual(response[1], 400,
                             'Returned unexpected status code')

    def test_reserve(self):
        with self.app_context():
            book = Book.query.first()
            # Reserve a book
            expected = {
                'book': 'Test Book',
                'user': 'Test Borrower',
                'date_begin': date.today(),
                'date_end': None
            }
            self.assertDictEqual(ut.reserve(book, 2), expected,
                                 'Unable to reserve a book')

            # Attempt to reserve a book that is already reserved
            response = ut.reserve(book, 2)
            self.assertDictEqual(response[0], ut.unavailable_message,
                                 'Did not return correct message when attempted to reserve an unavailable book')
            self.assertEqual(response[1], 400,
                             'Returned unexpected status code')

    def test_reserve_checked_out(self):
        with self.app_context():
            book = Book.query.first()
            # Attempt to reserve a book that is checked out
            ut.save_to_db(Lending(book_id=1, user_id=1))
            response = ut.reserve(book, 2)
            self.assertDictEqual(response[0], ut.unavailable_message,
                                 'Did not return correct message when attempted to reserve an unavailable book')
            self.assertEqual(response[1], 400,
                             'Returned unexpected status code')

    def test_reserve_inactive(self):
        with self.app_context():
            book = Book.query.first()
            # Attempt to reserve an inactive book
            book.active = False
            ut.save_to_db(book)
            response = ut.reserve(book, 2)
            self.assertDictEqual(response[0], ut.unavailable_message,
                                 'Did not return correct message when attempted to reserve an inactive book')
            self.assertEqual(response[1], 400,
                             'Returned unexpected status code')

    def test_release_return(self):
        with self.app_context():
            book = Book.query.first()

            # Attempt to return a book that has not been lent
            expected1 = {'message': 'book is not checked out'}
            response = ut.release(book, 1, 'return')
            self.assertDictEqual(response[0], expected1,
                                 'Did not return correct message when attempted to return an invalid book')
            self.assertEqual(response[1], 400,
                             'Returned unexpected status code')

            # Mark a book as returned as the book owner
            ut.save_to_db(Lending(book_id=1, user_id=2))
            expected2 = {'message': 'book is now available'}
            self.assertDictEqual(ut.release(book, 1, 'return'), expected2,
                                 'Unable to mark book as returned as a book owner')

            # Return a borrowed book
            ut.save_to_db(Lending(book_id=1, user_id=2))
            self.assertDictEqual(ut.release(book, 2, 'return'), expected2,
                                 'Unable to return a borrowed book')

            # Attempt to return a book without authorization
            malicious_user = User(
                username='test',
                password='test',
                lender=True,
                borrower=False
            )
            ut.save_to_db(malicious_user)
            ut.save_to_db(Lending(book_id=1, user_id=2))
            expected3 = {'message': 'unauthorized'}
            response = ut.release(book, 3, 'return')
            self.assertDictEqual(response[0], expected3,
                                 'Did not return error when attempting to return a book unauthorized')
            self.assertEqual(response[1], 401,
                             'Returned unexpected status code')

    def test_release_cancel(self):
        with self.app_context():
            book = Book.query.first()

            # Attempt to cancel the reservation on a book that has not been reserved
            expected1 = ({'message': 'book has not been reserved'}, 400)
            self.assertTupleEqual(ut.release(book, 1, 'cancel'), expected1,
                                  'Did not return error when attempting to cancel a reservation for a unreserved book')

            # Cancel a reservation as a book owner
            ut.save_to_db(Reservation(book_id=1, user_id=2))
            expected2 = {'message': 'book is now available'}
            self.assertDictEqual(ut.release(book, 1, 'cancel'), expected2,
                                 'Unable to cancel reservation as a book owner')

            # Cancel a previously made reservation
            ut.save_to_db(Reservation(book_id=1, user_id=2))
            self.assertDictEqual(ut.release(book, 2, 'cancel'), expected2,
                                 'Unable to cancel reservation as the user who initiated the reservation')

            # Attempt to cancel a reservation without authorization
            malicious_user = User(
                username='test',
                password='test',
                lender=True,
                borrower=False
            )
            ut.save_to_db(malicious_user)
            ut.save_to_db(Reservation(book_id=1, user_id=2))
            expected3 = {'message': 'unauthorized'}
            response = ut.release(book, 3, 'cancel')
            self.assertDictEqual(response[0], expected3,
                                 'Did not return error when attempting to cancel a reservation unauthorized')
            self.assertEqual(response[1], 401,
                             'Returned unexpected status code')

    def test_get_active_lending(self):
        with self.app_context():
            book = Book.query.first()

            # Attempt to get an active lending when there are none
            lending1 = Lending(
                book_id=1,
                user_id=2,
                date_begin=date(year=2021, month=3, day=27),
                date_end=date(year=2021, month=4, day=7)
            )
            ut.save_to_db(lending1)
            self.assertIsNone(ut.get_active_lending(book),
                              'Found an active lending, but expected not to.')

            # Get an active lending when it exists
            lending2 = Lending(
                book_id=1,
                user_id=2
            )
            ut.save_to_db(lending2)
            self.assertEqual(ut.get_active_lending(book), lending2,
                             'Returned unexpected information')

    def test_get_active_reservation(self):
        with self.app_context():
            book = Book.query.first()

            # Attempting to get an active reservation when there are none
            reservation1 = Reservation(
                book_id=1,
                user_id=2,
                date_begin=date(year=2021, month=3, day=27),
                date_end=date(year=2021, month=4, day=7)
            )
            ut.save_to_db(reservation1)
            self.assertIsNone(ut.get_active_reservation(book),
                              'Found an active reservation, but expected not to.')

            # Getting an active reservation when it exists
            reservation2 = Reservation(
                book_id=1,
                user_id=2
            )
            ut.save_to_db(reservation2)

            self.assertEqual(ut.get_active_reservation(book), reservation2,
                             'Returned unexpected information')

    def test_print_book(self):
        with self.app_context():
            book = Book.query.first()
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
            self.assertDictEqual(ut.print_book(book), expected,
                                 'Returned unexpected information')

    def test_print_book_list(self):
        with self.app_context():
            books = Book.query.all()
            expected = {
                'books': [
                    {
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
                ]
            }
            self.assertDictEqual(ut.print_book_list(books), expected,
                                 'Returned unexpected information')
