class Book:
    def __init__(self, _id, title, author, year):
        self.id = _id
        self.title = title
        self.author = author
        self.year = year
        self.active = True


class LendedBook():
    pass


class ReservedBook():
    pass


class User:
    def __init__(self, _id, username, password, lender, borrower):
        self.id = _id
        self.username = username
        self.password = password
        self.lender = lender
        self.borrower = borrower
