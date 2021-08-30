from datetime import date

from models import Lending


def book_checkout(book, borrower_id):
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


def book_checkin(book):
    current_lending = None

    for lending in book.lendings.all():
        if not lending.date_end:
            current_lending = lending

    if not current_lending:
        return {'message': 'book has not been checked out'}, 400

    current_lending.date_end = date.today()
    current_lending.save_to_db()

    return lending.json()
