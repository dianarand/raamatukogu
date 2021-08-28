import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


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
            "author": row[2]
        }
        books.append(book)

    connection.close()
    return jsonify({'books': books})


@app.route('/books', methods=['POST'])
def add_book():  # Create a new book
    data = request.get_json()

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = 'INSERT INTO books VALUES (NULL, ?, ?, ?, ?)'
    cursor.execute(query, (data['title'], data['author'], data['year'], 1))

    connection.commit()
    connection.close()

    return {'message': 'book added successfully'}, 201


@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):  # Get a book
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = 'SELECT * FROM books WHERE id=?'
    result = cursor.execute(query, (book_id,))
    row = result.fetchone()

    if row:
        book = {
            "id": row[0],
            "title": row[1],
            "author": row[2]
        }
    else:
        book = None

    connection.close()

    return book


@app.route('/book/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):  # Remove a book
    # books[book_id]['active'] = False
    # return jsonify(books[book_id])
    pass


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
