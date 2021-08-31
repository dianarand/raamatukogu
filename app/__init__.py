from flask import Flask
from flask_jwt import JWT

from app.db import db
from app.config import Config
from app.security import authenticate, identity

app = Flask(__name__)
app.config.from_object(Config)


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)

jwt = JWT(app, authenticate, identity)

from app import routes
