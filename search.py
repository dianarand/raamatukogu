from models import Book, Lending, Reservation


def by_title(curr_result, title):
    curr_result = query_setup(curr_result)
    curr_result = curr_result.filter(Book.title.like(searchf(title)))
    return curr_result


def by_author(curr_result, author):
    curr_result = query_setup(curr_result)
    curr_result = curr_result.filter(Book.author.like(searchf(author)))
    return curr_result


def by_year(curr_result, year):
    curr_result = query_setup(curr_result)
    curr_result = curr_result.filter_by(year=int(year))
    return curr_result


def by_filter(curr_result, fltr, user_id):
    curr_result = query_setup(curr_result)
    if fltr == 'owned_by_me':
        return books_owned_by_me(curr_result, user_id)
    if fltr == 'borrowed_by_me':
        return books_borrowed_by_me(curr_result, user_id)
    if fltr == 'reserved_by_me':
        return books_reserved_by_me(curr_result, user_id)


def books_owned_by_me(curr_result, user_id):
    curr_result = curr_result.filter_by(owner_id=user_id)
    return curr_result


def books_borrowed_by_me(curr_result, user_id):
    curr_result = curr_result.join(Lending).filter_by(user_id=user_id, date_end=None)
    return curr_result


def books_reserved_by_me(curr_result, user_id):
    curr_result = curr_result.join(Reservation).filter_by(user_id=user_id, date_end=None)
    return curr_result


def searchf(arg):
    return '%{}%'.format(arg)


def query_setup(curr_result):
    if not curr_result:
        curr_result = Book.query
    return curr_result
