from flask import Flask, request
from db import db
from models import Book, Lending, Reservation, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)


@app.route('/books', methods=['GET'])
def get_book_list():  # Get a list of books
    return {'items': [book.json() for book in Book.query.all()]}


@app.route('/books', methods=['POST'])
def add_book():  # Create a new book
    data = request.get_json()
    book = Book(data['title'], data['author'], data['year'], 1)
    book.save_to_db()
    return {'message': 'book added successfully'}, 201


@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):  # Get a book
    result = Book.query.filter_by(id=book_id).first()
    return result.json()


@app.route('/book/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):  # Remove a book
    result = Book.query.filter_by(id=book_id).first()
    result.active = 0
    result.save_to_db()
    return result.json()


@app.route('/borrow', methods=['POST'])
def borrow_book():  # Borrow a book
    data = request.get_json()

    user_id = data['user_id']
    user = User.query.filter_by(id=user_id).first()
    if not user.borrower:
        return {'message': 'cannot borrow book'}

    book_id = data['book_id']
    book = Book.query.filter_by(id=book_id).first()

    if not book.check_availability():
        return {'message': 'book not available'}

    lending = Lending(book_id, data['user_id'])
    lending.save_to_db()
    return lending.json()


@app.route('/return', methods=['POST'])
def return_book():  # Return a book
    pass


@app.route('/reserve', methods=['POST'])
def reserve_book():  # Reserve a book
    data = request.get_json()

    user_id = data['user_id']
    user = User.query.filter_by(id=user_id).first()
    if not user.borrower:
        return {'message': 'cannot reserve book'}

    book_id = data['book_id']
    book = Book.query.filter_by(id=book_id).first()

    if not book.check_availability():
        return {'message': 'book not available'}

    reservation = Reservation(book_id, data['user_id'])
    reservation.save_to_db()

    return reservation.json()


@app.route('/cancel', methods=['POST'])
def cancel_reservation():  # Cancel a reservation
    pass


if __name__ == '__main__':
    app.run(debug=True)
