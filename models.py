from db import db
from datetime import date, timedelta


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    year = db.Column(db.Integer)
    active = db.Column(db.Integer)

    lendings = db.relationship('Lending', lazy='dynamic')
    reservations = db.relationship('Reservation', lazy='dynamic')

    def __init__(self, title, author, year, active):
        self.title = title
        self.author = author
        self.year = year
        self.active = active

    def json(self):
        result = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'active': bool(self.active)
        }
        return result

    def check_availability(self):
        if not self.active:
            return False
        for lending_data in self.lendings.all():
            if not lending_data.date_end:
                return False
        for reservation_data in self.reservations.all():
            if not reservation_data.date_end:
                return False
        return True

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Lending(db.Model):
    __tablename__ = 'lendings'

    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship('Book')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    date_begin = db.Column(db.Date, default=date.today())
    date_end = db.Column(db.Date)
    deadline = db.Column(db.Date)

    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id
        self.deadline = date.today() + timedelta(weeks=4)

    def json(self):
        result = {
            "book": self.book.title,
            "user": self.user.username,
            "date_begin": self.date_begin,
            "date_end": self.date_end,
            "deadline": self.deadline
        }
        return result

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship('Book')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    date_begin = db.Column(db.Date, default=date.today())
    date_end = db.Column(db.Date)

    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id

    def json(self):
        result = {
            "book": self.book.title,
            "user": self.user.username,
            "date_begin": self.date_begin,
        }
        return result

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    lender = db.Column(db.Integer)
    borrower = db.Column(db.Integer)

    def __init__(self, username, password, lender, borrower):
        self.username = username
        self.password = password
        self.lender = lender
        self.borrower = borrower

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
