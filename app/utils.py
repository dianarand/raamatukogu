from datetime import date

from app.db import db
from app.models import Lending, Reservation

unavailable_message = {'message': 'book unavailable'}


def checkout(book, borrower_id):  # check a book out from the library
    if not book.active or get_active_lending(book):
        return unavailable_message, 400

    reservation = get_active_reservation(book)
    if reservation:
        if reservation.user_id == borrower_id:
            reservation.date_end = date.today()
        else:
            return unavailable_message, 400

    lending = Lending(
        book_id=book.id,
        user_id=borrower_id
    )
    save_to_db(lending)

    lending_json = print_usage(lending)
    lending_json.update({'deadline': lending.deadline})

    return lending_json


def reserve(book, user_id):
    if not book.active or get_active_lending(book) or get_active_reservation(book):
        return unavailable_message, 400

    reservation = Reservation(
        book_id=book.id,
        user_id=user_id
    )
    save_to_db(reservation)

    return print_usage(reservation)


def release(book, user_id, usage):  # release a book from a user
    if usage == 'return':
        current_use = get_active_lending(book)
        if not current_use:
            return {'message': 'book is not checked out'}, 400

    elif usage == 'cancel':
        current_use = get_active_reservation(book)
        if not current_use:
            return {'message': 'book has not been reserved'}, 400

    if user_id != book.owner_id and user_id != current_use.user_id:
        return {'message': 'unauthorized'}, 401

    current_use.date_end = date.today()
    save_to_db(current_use)

    return print_usage(current_use), 200


def get_active_lending(book):
    return book.lendings.filter_by(date_end=None).first()


def get_active_reservation(book):
    return book.reservations.filter_by(date_end=None).first()


def print_book(book):  # return book information to JSON
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'owner': book.owner.username,
        'active': book.active
    }


def print_book_list(books, check_overtime=False):
    book_list = []
    for book in books:
        book_data = print_book(book)

        if check_overtime:
            overtime = False
            lending = get_active_lending(book)
            if lending:
                if lending.deadline < date.today():
                    overtime = True
            book_data.update({'overtime': overtime})

        book_list.append(book_data)

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
