from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash

from db import db
from config import Config
from models import Book, Lending, Reservation, User
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
    return {'items': [book.json() for book in Book.query.all()]}


@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():  # Create a new book
    if not current_identity.lender:
        return {'message': 'not authorized'}, 401
    data = request.get_json()
    book = Book(data['title'], data['author'], data['year'], current_identity.id)
    book.save_to_db()
    return {'message': 'book added successfully'}, 201


@app.route('/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):  # Get a book
    result = Book.query.filter_by(id=book_id).first()
    return result.json()


@app.route('/book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def remove_book(book_id):  # Remove a book
    if not current_identity.lender:
        return {'message': 'not authorized'}, 401
    result = Book.query.filter_by(id=book_id).first()
    result.active = 0
    result.save_to_db()
    return result.json()


# WORK IN PROGRESS
# @app.route('/book/<int:book_id>/lend', methods=['POST'])
# @jwt_required()
# def lend_book(book_id):  # Borrow a book
#     data = request.get_json()
#     borrower_id = data['borrower_id']
#
#     if not current_identity.lender:
#         return {'message': 'not authorized'}, 401
#
#     user = User.query.filter_by(id=borrower_id).first()
#
#     if not user.borrower:
#         return {'message': 'invalid borrower'}, 400
#
#     book = Book.query.filter_by(id=book_id).first()
#
#     if not book.check_availability():
#         return {'message': 'book not available'}, 400
#
#     lending = Lending(book_id, current_identity.id)
#     lending.save_to_db()
#     return lending.json()


@app.route('/book/<int:book_id>/borrow', methods=['POST'])
@jwt_required()
def borrow_book(book_id):  # Borrow a book
    if not current_identity.borrower:
        return {'message': 'not authorized'}, 401

    book = Book.query.filter_by(id=book_id).first()

    if not book.check_availability():
        return {'message': 'book not available'}

    lending = Lending(book_id, current_identity.id)
    lending.save_to_db()
    return lending.json()


@app.route('/return', methods=['POST'])
@jwt_required()
def return_book():  # Return a book
    pass


@app.route('/reserve', methods=['POST'])
@jwt_required()
def reserve_book():  # Reserve a book
    data = request.get_json()

    if not current_identity.lender:
        return {'message': 'not authorized'}, 401

    book_id = data['book_id']
    book = Book.query.filter_by(id=book_id).first()

    if not book.check_availability():
        return {'message': 'book not available'}

    reservation = Reservation(book_id, current_identity.id)
    reservation.save_to_db()

    return reservation.json()


@app.route('/cancel', methods=['POST'])
@jwt_required()
def cancel_reservation():  # Cancel a reservation
    pass


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
    user = User(username, hashed_password, lender, borrower)
    user.save_to_db()
    return {'message': 'user created successfully'}, 201


if __name__ == '__main__':
    app.run(debug=True)
