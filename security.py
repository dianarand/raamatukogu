from models import User


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    user = User.query.filter_by(id=user_id).first()
    return user
