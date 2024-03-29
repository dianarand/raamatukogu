from flask import request
from flask_jwt import jwt_required, current_identity
from werkzeug.security import generate_password_hash

from app import app

from app.models import Book, User
from app.search import by_title, by_author, by_year, by_filter
from app.utils import checkout, reserve, release, get_active_lending, print_book, print_books, save_to_db


@app.route('/books', methods=['GET'])
@jwt_required()
def get_book_list():  # Get a list of books
    app.logger.info(f'User {current_identity.username} getting a list of books')
    query = request.args
    keys = query.keys()
    result = Book.query.filter_by(active=True)
    if 'title' in keys:
        result = by_title(result, query['title'])
    if 'author' in keys:
        result = by_author(result, query['author'])
    if 'year' in keys:
        result = by_year(result, query['year'])
    if 'filter' in keys:
        result = by_filter(result, query['filter'], current_identity.id)
    app.logger.info(f'SUCCESS : List of books returned to user {current_identity.username}')
    return print_books(result.all())


@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():  # Create a new book
    app.logger.info(f'User {current_identity.username} adding a new book')
    if not current_identity.lender:
        app.logger.info(f'FAIL : User {current_identity.username} is unauthorized')
        return {'message': 'Puuduvad õigused'}, 401

    data = request.get_json()
    try:
        book = Book(
            title=data['title'],
            author=data['author'],
            year=int(data['year']),
            owner_id=current_identity.id
        )
    except KeyError:
        app.logger.info(f'FAIL : User {current_identity.username} entered invalid data')
        return {'message': 'Puudulikud või vigased andmed'}, 400

    save_to_db(book)

    app.logger.info(f'SUCCESS : Book {book.title} added')
    return {'message': 'Raamat lisatud edukalt', 'id': book.id}, 201


@app.route('/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):  # Get a book
    app.logger.info(f'User {current_identity.username} getting book {book_id} information')
    book = Book.query.get(book_id)
    if not book:
        app.logger.info(f'FAIL : User {current_identity.username} queried book {book_id} not found')
        return {'message': 'Raamatut ei leitud'}, 404
    app.logger.info(f'SUCCESS : Book {book.title} information returned to user {current_identity.username}')
    return print_book(book)


@app.route('/book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def remove_book(book_id):  # Remove a book
    app.logger.info(f'User {current_identity.username} removing book {book_id}')
    if not current_identity.lender:
        app.logger.info(f'FAIL : User {current_identity.username} is unauthorized')
        return {'message': 'Puuduvad õigused'}, 401

    book = Book.query.get(book_id)

    if not book:
        app.logger.info(f'FAIL : User {current_identity.username} queried book {book_id} not found')
        return {'message': 'Raamatut ei leitud'}, 404

    if book.owner_id != current_identity.id:
        app.logger.info(f'FAIL : User {current_identity.username} is unauthorized')
        return {'message': 'Puuduvad õigused'}, 401

    if not book.active:
        app.logger.info(f'FAIL : User {current_identity.username} queried book {book.title} already removed')
        return {'message': 'Raamatut juba eemaldatud'}, 400

    if get_active_lending(book):
        app.logger.info(f'FAIL : User {current_identity.username} queried book {book.title} currently checked out')
        return {'message': 'Väljalaenutatud raamatut ei saa eemaldada'}, 400

    release(book, current_identity.id, 'cancel')

    book.active = False
    save_to_db(book)

    app.logger.info(f'SUCCESS : User {current_identity.username} removed book {book.title} successfully')
    return {'message': 'Raamat eemaldatud edukalt'}


@app.route('/book/<int:book_id>/lend', methods=['POST'])
@jwt_required()
def lend_book(book_id):  # Lend a book
    app.logger.info(f'User {current_identity.username} lending out a book {book_id}')
    data = request.get_json()
    try:
        username = data['borrower']
    except (KeyError, TypeError):
        app.logger.info(f'FAIL : User {current_identity.username} entered invalid data')
        return {'message': 'Puudulikud või vigased andmed'}, 400

    if not current_identity.lender:
        app.logger.info(f'FAIL : User {current_identity.username} is unauthorized')
        return {'message': 'Puuduvad õigused'}, 401

    user = User.query.filter_by(username=username).first()

    if not user:
        app.logger.info(f'FAIL : User {current_identity.username} queried user {username} not found')
        return {'message': 'Kasutajat ei leitud'}, 404

    if not user.borrower:
        app.logger.info(f'FAIL : User {user.borrower} not a valid borrower')
        return {'message': 'Ebasobiv laenutaja'}, 400

    book = current_identity.owned_books.filter_by(id=book_id).first()
    if not book:
        app.logger.info(f'FAIL : User {current_identity.username} queried book {book_id} not found')
        return {'message': 'Raamatut ei leitud'}, 404

    if 'weeks' in data.keys():
        return checkout(book, user.id, data['weeks'])

    return checkout(book, user.id)


@app.route('/book/<int:book_id>/borrow', methods=['POST'])
@jwt_required()
def borrow_book(book_id):  # Borrow a book
    app.logger.info(f'User {current_identity.username} borrowing a book')
    if not current_identity.borrower:
        app.logger.info(f'FAIL : User {current_identity.username} is unauthorized')
        return {'message': 'Puuduvad õigused'}, 401

    book = Book.query.get(book_id)

    if not book:
        app.logger.info(f'FAIL : User {current_identity.username} queried book {book_id} not found')
        return {'message': 'Raamatut ei leitud'}, 404

    return checkout(book, current_identity.id)


@app.route('/book/<int:book_id>/return', methods=['POST'])
@jwt_required()
def return_book(book_id):  # Return a book
    app.logger.info(f'User {current_identity.username} returning a book')
    book = Book.query.get(book_id)

    if not book:
        app.logger.info(f'FAIL : User {current_identity.username} queried book {book_id} not found')
        return {'message': 'Raamatut ei leitud'}, 404

    return release(book, current_identity.id, 'return')


@app.route('/book/<int:book_id>/reserve', methods=['POST'])
@jwt_required()
def reserve_book(book_id):  # Reserve a book
    if not current_identity.borrower:
        app.logger.info(f'FAIL : User {current_identity.username} is unauthorized')
        return {'message': 'Puuduvad õigused'}, 401

    book = Book.query.get(book_id)

    if not book:
        app.logger.info(f'FAIL : User {current_identity.username} queried book {book_id} not found')
        return {'message': 'Raamatut ei leitud'}, 404

    return reserve(book, current_identity.id)


@app.route('/book/<int:book_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_reservation(book_id):  # Cancel a reservation
    app.logger.info(f'User {current_identity.username} canceling a reservation')
    book = Book.query.get(book_id)

    if not book:
        app.logger.info(f'FAIL : User {current_identity.username} queried book {book_id} not found')
        return {'message': 'Raamatut ei leitud'}, 404

    return release(book, current_identity.id, 'cancel')


@app.route('/register', methods=['POST'])
def register_user():  # Create a new user
    app.logger.info('Registering a new user')
    data = request.get_json()
    username = data['username']

    duplicates = User.query.filter_by(username=username).first()
    if duplicates:
        app.logger.info('FAIL : Duplicate username')
        return {'message': 'Kasutajanimi juba kasutuses'}, 400

    if data['role'] == 'lender':
        lender = True
        borrower = False
    elif data['role'] == 'borrower':
        lender = False
        borrower = True
    else:
        app.logger.info(f'FAIL : Invalid data entered')
        return {'message': 'Puudulikud või vigased andmed'}, 400

    hashed_password = generate_password_hash(data['password'])

    user = User(
        username=username,
        password=hashed_password,
        lender=lender,
        borrower=borrower
    )
    save_to_db(user)

    app.logger.info(f'SUCCESS : User {user.username} created')
    return {'message': 'Kasutaja loodud edukalt'}, 201
