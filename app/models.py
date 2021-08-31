from app.db import db
from datetime import date, timedelta


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    year = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    lendings = db.relationship('Lending', backref='book', lazy='dynamic')
    reservations = db.relationship('Reservation', backref='book', lazy='dynamic')


class Lending(db.Model):
    __tablename__ = 'lendings'

    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    date_begin = db.Column(db.Date, default=date.today())
    date_end = db.Column(db.Date)
    deadline = db.Column(db.Date, default=(date.today()+timedelta(weeks=4)))


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    date_begin = db.Column(db.Date, default=date.today())
    date_end = db.Column(db.Date)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    lender = db.Column(db.Boolean)
    borrower = db.Column(db.Boolean)

    owned_books = db.relationship('Book', backref='owner', lazy='dynamic')
