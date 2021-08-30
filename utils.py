from datetime import date

from db import db
from models import Lending, Reservation

unavailable_message = {'message': 'book unavailable'}


def checkout(book, borrower_id):  # check a book out from the library
    if not book.active:
        return unavailable_message, 400

    for lending in book.lendings.all():
        if not lending.date_end:
            return unavailable_message, 400

    for reservation in book.reservations.all():
        if not reservation.date_end:
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
    if not book.active:
        return unavailable_message, 400

    for lending in book.lendings.all():
        if not lending.date_end:
            return unavailable_message, 400

    for reservation in book.reservations.all():
        if not reservation.date_end:
            return unavailable_message, 400

    reservation = Reservation(
        book_id=book.id,
        user_id=user_id
    )
    save_to_db(reservation)

    return print_usage(reservation)


def release(book, user_id, usage):  # release a book from a user
    current_use = None

    if usage == 'return':
        for lending in book.lendings.all():
            if not lending.date_end:
                current_use = lending
        if not current_use:
            return {'message': 'book is not checked out'}, 400

    elif usage == 'cancel':
        for reservation in book.reservations.all():
            if not reservation.date_end:
                current_use = reservation
        if not current_use:
            return {'message': 'book has not been reserved'}, 400

    if user_id != book.owner_id and user_id != current_use.user_id:
        return {'message': 'unauthorized'}, 401

    current_use.date_end = date.today()
    save_to_db(current_use)

    return print_usage(current_use)


def print_book(book):  # return book information to JSON
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'owner': book.owner.username,
        'active': book.active
    }


def print_book_list(books):
    book_list = []
    for book in books:
        book_data = print_book(book)
        overtime = False
        for lending in book.lendings:
            if lending.date_end:
                if lending.date_end > lending.deadline:
                    overtime = True
        book_data.update({'overtime': overtime})
        book_list.append(book_data)
    return {'books': book_list}


def print_usage(usage):  # return lending or reservation information to JSON
    return {
        "book": usage.book.title,
        "user": usage.user.username,
        "date_begin": usage.date_begin,
        "date_end": usage.date_end
    }


def save_to_db(item):  # save any object to database
    db.session.add(item)
    db.session.commit()
