import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_books = 'CREATE TABLE books (id INTEGER PRIMARY KEY, title text, author text, year int, active int)'
cursor.execute(create_books)

insert_books = 'INSERT INTO books VALUES (NULL, ?, ?, ?, ?)'

books = [
    ("Harry Potter and the Philosopher's Stone", "J. K. Rowling", 1997, 1),
    ("Harry Potter and the Chamber of Secrets", "J. K. Rowling", 1998, 1),
    ("Harry Potter and the Prisoner of Azkaban", "J. K. Rowling", 1999, 1),
]

cursor.executemany(insert_books, books)

select_books = 'SELECT * FROM books'
for row in cursor.execute(select_books):
    print(row)

print()

create_users = 'CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text, lender int, borrower int)'
cursor.execute(create_users)

insert_users = 'INSERT INTO users VALUES(NULL, ?, ?, ?, ?)'

users = [
    ("laenutaja", "parool1", 1, 0),
    ("laenaja", "parool2", 0, 1)
]

cursor.executemany(insert_users, users)

select_users = 'SELECT * FROM users'
for row in cursor.execute(select_users):
    print(row)

connection.commit()
connection.close()
