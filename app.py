from flask import Flask, request, jsonify

app = Flask(__name__)

books = []


@app.route('/books', methods=['GET'])
def get_book_list():  # Get a list of books
    return jsonify({'books': books})


@app.route('/books', methods=['POST'])
def add_book():  # Create a new book
    data = request.get_json()
    new_book = {
        'title': data['title'],
        'author': data['author'],
        'year': data['year'],
        'active': True
    }
    books.append(new_book)
    return jsonify(new_book)


@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):  # Get a book
    return jsonify(books[book_id])


@app.route('/book/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):  # Remove a book
    books[book_id]['active'] = False
    return jsonify(books[book_id])


@app.route('/reserve', methods=['POST'])
def reserve_book():  # Reserve a book or cancel a reservation
    data = request.get_json()
    book_id = data['book_id']
    if not books[book_id]['active']:
        return jsonify({"message": "book not available"})
    pass


@app.route('/lend', methods=['POST'])
def lend_book():  # Lend or return a book
    pass


if __name__ == '__main__':
    app.run(debug=True)
