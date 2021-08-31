from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash

from db import db
from config import Config
from models import Book, User
from utils import checkout, reserve, release, print_book, print_book_list, save_to_db
from search import by_title, by_author, by_year, by_filter
from security import authenticate, identity

app = Flask(__name__)
app.config.from_object(Config)


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)

jwt = JWT(app, authenticate, identity)


@app.route('/books', methods=['GET'])
@jwt_required()
def get_book_list():  # Get a list of books
    query = request.args
    keys = query.keys()
    result = None
    if 'title' in keys:
        result = by_title(result, query['title'])
    if 'author' in keys:
        result = by_author(result, query['author'])
    if 'year' in keys:
        result = by_year(result, query['year'])
    if 'filter' in keys:
        result = by_filter(result, query['filter'], current_identity.id)
    if not result:
        result = Book.query
    return print_book_list(result.all(), True)


@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():  # Create a new book
    if not current_identity.lender:
        return {'message': 'not authorized'}, 401

    data = request.get_json()
    book = Book(
        title=data['title'],
        author=data['author'],
        year=int(data['year']),
        owner_id=current_identity.id
    )

    save_to_db(book)

    return {'message': 'book added successfully'}, 201


@app.route('/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):  # Get a book
    result = Book.query.filter_by(id=book_id).first()
    return print_book(result)


@app.route('/book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def remove_book(book_id):  # Remove a book
    if not current_identity.lender:
        return {'message': 'not authorized'}, 401

    book = Book.query.filter_by(id=book_id).first()

    if book.owner_id != current_identity.id:
        return {'message': 'not authorized'}, 401

    if not book.active:
        return {'message': 'book already removed'}, 400

    for reservation in book.reservations.all():
        if not reservation.date_end:
            release(book, current_identity.id, 'cancel')

    book.active = False
    save_to_db(book)

    return print_book(book)


@app.route('/book/<int:book_id>/lend', methods=['POST'])
@jwt_required()
def lend_book(book_id):  # Lend a book
    data = request.get_json()
    borrower_id = data['borrower_id']

    if not current_identity.lender:
        return {'message': 'not authorized'}, 401

    user = User.query.filter_by(id=borrower_id).first()

    if not user.borrower:
        return {'message': 'invalid borrower'}, 400

    for owned_book in current_identity.owned_books.all():
        if owned_book.id == book_id:
            return checkout(owned_book, borrower_id)

    return {'message': 'not authorized'}, 401


@app.route('/book/<int:book_id>/borrow', methods=['POST'])
@jwt_required()
def borrow_book(book_id):  # Borrow a book
    if not current_identity.borrower:
        return {'message': 'not authorized'}, 401

    book = Book.query.filter_by(id=book_id).first()

    return checkout(book, current_identity.id)


@app.route('/book/<int:book_id>/return', methods=['POST'])
@jwt_required()
def return_book(book_id):  # Return a book
    book = Book.query.filter_by(id=book_id).first()
    return release(book, current_identity.id, 'return')


@app.route('/book/<int:book_id>/reserve', methods=['POST'])
@jwt_required()
def reserve_book(book_id):  # Reserve a book
    if not current_identity.borrower:
        return {'message': 'not authorized'}, 401

    book = Book.query.filter_by(id=book_id).first()

    return reserve(book, current_identity.id)


@app.route('/book/<int:book_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_reservation(book_id):  # Cancel a reservation
    book = Book.query.filter_by(id=book_id).first()
    return release(book, current_identity.id, 'cancel')


@app.route('/register', methods=['POST'])
def register_user():  # Create a new user
    data = request.get_json()
    username = data['username']

    duplicates = User.query.filter_by(username=username).first()
    if duplicates:
        return {'message': 'username already in use'}

    if data['role'] == 'lender':
        lender = True
        borrower = False
    elif data['role'] == 'borrower':
        lender = False
        borrower = True

    hashed_password = generate_password_hash(data['password'])

    user = User(
        username=username,
        password=hashed_password,
        lender=lender,
        borrower=borrower
    )
    save_to_db(user)

    return {'message': 'user created successfully'}, 201


if __name__ == '__main__':
    app.run(debug=True)
