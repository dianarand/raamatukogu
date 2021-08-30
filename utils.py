from datetime import date

from models import Lending, Reservation


def checkout(book, borrower_id):  # check a book out from the library
    if not book.active:
        return {'message': 'book unavailable'}, 400

    for lending in book.lendings.all():
        if not lending.date_end:
            return {'message': 'book unavailable'}, 400

    for reservation in book.reservations.all():
        if not reservation.date_end:
            if reservation.user_id == borrower_id:
                reservation.date_end = date.today()
            else:
                return {'message': 'book unavailable'}, 400

    lending = Lending(book.id, borrower_id)
    lending.save_to_db()

    return lending.json()


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
    current_use.save_to_db()

    return current_use.json()


def reserve(book, user_id):
    if not book.active:
        return {'message': 'book unavailable'}, 400

    for lending in book.lendings.all():
        if not lending.date_end:
            return {'message': 'book unavailable'}, 400

    for reservation in book.reservations.all():
        if not reservation.date_end:
            return {'message': 'book unavailable'}, 400

    reservation = Reservation(book.id, user_id)
    reservation.save_to_db()

    return reservation.json()
