from datetime import date, timedelta

from app import app
from app.db import db
from app.models import Lending, Reservation

unavailable_message = {'message': 'Raamat pole saadaval'}


def checkout(book, borrower_id, weeks=None):  # check a book out from the library
    if not book.active or get_active_lending(book):
        app.logger.info(f'FAIL : Book {book.title} unavailable')
        return unavailable_message, 400

    reservation = get_active_reservation(book)
    if reservation:
        if reservation.user_id == borrower_id:
            reservation.date_end = date.today()
        else:
            app.logger.info(f'FAIL : Book {book.title} unavailable')
            return unavailable_message, 400

    lending = Lending(
        book_id=book.id,
        user_id=borrower_id
    )

    if weeks:
        lending.deadline = date.today()+timedelta(weeks=weeks)

    save_to_db(lending)

    lending_json = print_usage(lending)
    lending_json.update({
        'deadline': lending.deadline,
        'message': 'Raamat edukalt laenutatud'
    })

    app.logger.info(f'SUCCESS : Book {book.title} borrowed to user {borrower_id}')
    return lending_json


def reserve(book, user_id):
    if not book.active or get_active_lending(book) or get_active_reservation(book):
        app.logger.info(f'FAIL : Book {book.title} unavailable')
        return unavailable_message, 400

    reservation = Reservation(
        book_id=book.id,
        user_id=user_id
    )
    save_to_db(reservation)

    app.logger.info(f'SUCCESS : Book {book.title} reserved by user {user_id}')
    lending_json = print_usage(reservation)
    lending_json.update({'message': 'Raamat edukalt broneeritud'})
    return lending_json


def release(book, user_id, usage):  # release a book from a user
    if usage == 'return':
        current_use = get_active_lending(book)
        if not current_use:
            app.logger.info(f'FAIL : Book {book.title} not checked out')
            return {'message': 'Raamat ei ole välja laenatud'}, 400

    elif usage == 'cancel':
        current_use = get_active_reservation(book)
        if not current_use:
            app.logger.info(f'FAIL : Book {book.title} not reserved')
            return {'message': 'Raamat ei ole broneeritud'}, 400

    if user_id != book.owner_id and user_id != current_use.user_id:
        app.logger.info(f'FAIL : User {user_id} is unauthorized')
        return {'message': 'Puuduvad õigused'}, 401

    current_use.date_end = date.today()
    save_to_db(current_use)

    app.logger.info(f'SUCCESS : Book {book.title} is made available')
    return {'message': 'Raamat on nüüd saadaval'}


def get_active_lending(book):
    return book.lendings.filter_by(date_end=None).first()


def get_active_reservation(book):
    return book.reservations.filter_by(date_end=None).first()


def print_book(book):  # return book information to JSON
    data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'owner': book.owner.username,
        'active': book.active,
        'lending': None,
        'deadline': None,
        'overtime': False,
        'reservation': None
    }
    lending = get_active_lending(book)
    if lending:
        data.update({'lending': lending.user.username,
                     'deadline': lending.deadline})
        if lending.deadline < date.today():
            data.update({'overtime': True})
    else:
        reservation = get_active_reservation(book)
        if reservation:
            data.update({'reservation': reservation.user.username})
    return data


def print_books(books):
    book_list = []
    for book in books:
        book_list.append(print_book(book))
    return {'books': book_list}


def print_usage(usage):  # return lending or reservation information to JSON
    return {
        'book': usage.book.title,
        'user': usage.user.username,
        'date_begin': usage.date_begin,
        'date_end': usage.date_end
    }


def save_to_db(item):  # save any object to database
    db.session.add(item)
    db.session.commit()
