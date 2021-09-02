from flask import request
from flask_jwt import jwt_required, current_identity
from werkzeug.security import generate_password_hash

from app import app

from app.models import Book, User
from app.search import by_title, by_author, by_year, by_filter
from app.utils import checkout, reserve, release, print_book, print_book_list, save_to_db


@app.route('/books', methods=['GET'])
@jwt_required()
def get_book_list():  # Get a list of books
    app.logger.info(f'User id={current_identity.id} getting a list of books')
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
    app.logger.info('SUCCESS')
    return print_book_list(result.all(), True)


@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():  # Create a new book
    app.logger.info(f'User id={current_identity.id} adding a new book')
    if not current_identity.lender:
        app.logger.info('FAIL : Unauthorized')
        return {'message': 'unauthorized'}, 401

    data = request.get_json()
    try:
        book = Book(
            title=data['title'],
            author=data['author'],
            year=int(data['year']),
            owner_id=current_identity.id
        )
    except KeyError:
        app.logger.info('FAIL : Invalid data')
        return {'message': 'invalid data posted'}, 400

    save_to_db(book)

    app.logger.info(f'SUCCESS : Book id={book.id} added')
    return {'message': 'book added successfully'}, 201


@app.route('/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):  # Get a book
    app.logger.info(f'User id={current_identity.id} getting book information')
    result = Book.query.filter_by(id=book_id).first()
    if not result:
        app.logger.info(f'FAIL : Book id={book_id} not found')
        return {'message': 'book not found'}, 404
    app.logger.info(f'SUCCESS : Book id={book_id} found')
    return print_book(result)


@app.route('/book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def remove_book(book_id):  # Remove a book
    app.logger.info(f'User id={current_identity.id} removing a book')
    if not current_identity.lender:
        app.logger.info('FAIL : Unauthorized')
        return {'message': 'unauthorized'}, 401

    book = Book.query.filter_by(id=book_id).first()

    if not book:
        app.logger.info(f'FAIL : Book id={book_id} not found')
        return {'message': 'book not found'}, 404

    if book.owner_id != current_identity.id:
        app.logger.info('FAIL : Unauthorized')
        return {'message': 'unauthorized'}, 401

    if not book.active:
        app.logger.info(f'FAIL : Book id={book_id} already removed')
        return {'message': 'book already removed'}, 400

    release(book, current_identity.id, 'cancel')

    book.active = False
    save_to_db(book)

    app.logger.info(f'SUCCESS : Book id={book_id} removed')
    return {'message': 'book successfully removed'}


@app.route('/book/<int:book_id>/lend', methods=['POST'])
@jwt_required()
def lend_book(book_id):  # Lend a book
    app.logger.info(f'User id={current_identity.id} lending a book')
    data = request.get_json()
    try:
        borrower_id = data['borrower_id']
    except KeyError:
        app.logger.info('FAIL : Invalid data')
        return {'message': 'invalid data'}, 400

    if not current_identity.lender:
        app.logger.info('FAIL : Unauthorized')
        return {'message': 'unauthorized'}, 401

    user = User.query.filter_by(id=borrower_id).first()

    if not user:
        app.logger.info(f'FAIL : User id={borrower_id} not found')
        return {'message': 'user not found'}, 404

    if not user.borrower:
        app.logger.info(f'FAIL : User id={borrower_id} not a valid borrower')
        return {'message': 'invalid borrower'}, 400

    book = current_identity.owned_books.filter_by(id=book_id).first()
    if book:
        return checkout(book, borrower_id)

    app.logger.info(f'FAIL : Book id={book_id} not found')
    return {'message': 'book not found'}, 404


@app.route('/book/<int:book_id>/borrow', methods=['POST'])
@jwt_required()
def borrow_book(book_id):  # Borrow a book
    app.logger.info(f'User id={current_identity.id} borrowing a book')
    if not current_identity.borrower:
        app.logger.info('FAIL : Unauthorized')
        return {'message': 'unauthorized'}, 401

    book = Book.query.filter_by(id=book_id).first()

    if not book:
        app.logger.info(f'FAIL : Book id={book_id} not found')
        return {'message': 'book not found'}, 404

    return checkout(book, current_identity.id)


@app.route('/book/<int:book_id>/return', methods=['POST'])
@jwt_required()
def return_book(book_id):  # Return a book
    app.logger.info(f'User id={current_identity.id} returning a book')
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        app.logger.info(f'FAIL : Book id={book_id} not found')
        return {'message': 'book not found'}, 404

    return release(book, current_identity.id, 'return')


@app.route('/book/<int:book_id>/reserve', methods=['POST'])
@jwt_required()
def reserve_book(book_id):  # Reserve a book
    if not current_identity.borrower:
        app.logger.info('FAIL : Unauthorized')
        return {'message': 'unauthorized'}, 401

    book = Book.query.filter_by(id=book_id).first()

    if not book:
        app.logger.info(f'FAIL : Book id={book_id} not found')
        return {'message': 'book not found'}, 404

    return reserve(book, current_identity.id)


@app.route('/book/<int:book_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_reservation(book_id):  # Cancel a reservation
    app.logger.info(f'User id={current_identity.id} canceling a reservation')
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        app.logger.info(f'FAIL : Book id={book_id} not found')
        return {'message': 'book not found'}, 404

    return release(book, current_identity.id, 'cancel')


@app.route('/register', methods=['POST'])
def register_user():  # Create a new user
    app.logger.info('Registering a new user')
    data = request.get_json()
    username = data['username']

    duplicates = User.query.filter_by(username=username).first()
    if duplicates:
        app.logger.info('FAIL : Duplicate username')
        return {'message': 'username already in use'}, 400

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

    app.logger.info(f'SUCCESS : User id={user.id} created')
    return {'message': 'user created successfully'}, 201
