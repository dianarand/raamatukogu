from datetime import timedelta


class Config:
    SECRET_KEY = '67935bee40960ace7c329c0cd8848a3d'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_URL_RULE = '/login'
    JWT_EXPIRATION_DELTA = timedelta(hours=8)
