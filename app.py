from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/books', methods=['GET'])
def get_booklist():  # Get a list of books
    pass


@app.route('/books', methods=['POST'])
def add_book():  # Create a new book
    pass


@app.route('/book/<int:book_id>', methods=['GET'])
def get_book():  # Get a book
    pass


@app.route('/book/<int:book_id>', methods=['DELETE'])
def remove_book():  # Remove a book
    pass


@app.route('/reserve', methods=['POST'])
def reserve_book():  # Reserve a book or cancel a reservation
    pass


@app.route('lend', methods=['POST'])
def lend_book():  # Lend or return a book
    pass


if __name__ == '__main__':
    app.run(debug=True)
