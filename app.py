import sqlite3
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
# from db import db
from models import Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


@app.route('/books', methods=['GET'])
def get_book_list():  # Get a list of books
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM books')

    books = []
    for row in result:
        book = {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "year": row[3],
            "active": bool(row[4])
        }
        books.append(book)

    connection.close()
    return {'books': books}


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


@app.route('/reserve', methods=['POST'])
def reserve_book():  # Reserve a book or cancel a reservation
    # data = request.get_json()
    # book_id = data['book_id']
    # if not books[book_id]['active']:
    #     return jsonify({"message": "book not available"})
    pass


@app.route('/lend', methods=['POST'])
def lend_book():  # Lend or return a book
    pass


if __name__ == '__main__':
    app.run(debug=True)
