from datetime import date

from models import Book, Lending


def book_checkout(book_id, borrower_id):
    book = Book.query.filter_by(id=book_id).first()

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

    lending = Lending(book_id, borrower_id)
    lending.save_to_db()

    return lending.json()
