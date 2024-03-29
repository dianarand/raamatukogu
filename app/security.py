from werkzeug.security import check_password_hash
from app.models import User


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    user = User.query.filter_by(id=user_id).first()
    return user
