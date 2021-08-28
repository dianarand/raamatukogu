from db import db


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    year = db.Column(db.Integer)
    active = db.Column(db.Integer)

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class LentBook:
    pass


class ReservedBook:
    pass


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    lender = db.Column()
    borrower = db.Column()

    def __init__(self, _id, username, password, lender, borrower):
        self.id = _id
        self.username = username
        self.password = password
        self.lender = lender
        self.borrower = borrower
