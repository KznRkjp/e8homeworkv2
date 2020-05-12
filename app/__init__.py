from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



def create_app():
    app = Flask(__name__)
    POSTGRES_URL = 'db:5432'
    #POSTGRES_URL = 'localhost:5432'
    POSTGRES_USER = 'user'
    POSTGRES_PW = 'pass'
    POSTGRES_DB = 'test'
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CELERY_BROKER_URL'] = 'redis://redis:6379'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379'
    #app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
    #app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
    app.config.timezone   = 'Europe/Moscow'
    app.config.enable_utc   = True
    app.debug = True
    return app

app = create_app()
db = SQLAlchemy(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'],)
celery.conf.update(app.config)

from app import application, get_page
db.create_all()
