
from flask import render_template, request, redirect
from .get_page import test_func, clean_list, count
from urllib.parse import urlparse
from datetime import datetime
import enum
from app import app, db, celery



class Results(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    taskid = db.Column(db.Integer, unique=False, nullable=True)
    address = db.Column(db.String(300), unique=False, nullable=True)
    words_count = db.Column(db.Integer, unique=False, nullable=True)
    http_status_code = db.Column(db.Integer)

class TaskStatus (enum.Enum):
    NOT_STARTED = 1
    PENDING = 2
    FINISHED = 3

class Tasks(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300), unique=False, nullable=True)
    timestamp = db.Column(db.DateTime())
    task_status = db.Column(db.Enum(TaskStatus))
    http_status = db.Column(db.Integer)

#db.create_all()


@app.route('/')
def hello_world():
    search_results = Tasks.query.all()
    inspect_results = Results.query.all()
    return render_template('index.html', search_results = search_results, inspect_results = inspect_results)


@celery.task
def celery_test(dburlid, word):
    #from app import db
    print("fff")
    task = Tasks.query.get(dburlid)
    task.task_status = 'PENDING'
    db.session.commit()
    path = task.address
    # result = get_page.test_func(path, word)
    result = test_func(path, word)
    res = Results(taskid = dburlid, address = path, words_count = result['total'], http_status_code = result['http_status'])
    db.session.add(res)
    task.task_status = 'FINISHED'
    task.http_status = result['http_status']
    db.session.commit()


@app.route('/add-url', methods=['GET'])
def add_url():
    url = urlparse(request.args['url'])
    path = 'http://'+url.netloc+url.path+url.params+url.query

    #Пишем в базу
    db_url = Tasks(address = path, timestamp = datetime.now(tz=None), task_status = 'NOT_STARTED', http_status = 101)
    db.session.add(db_url)
    db.session.commit()
    # print(db_url._id," ",db_url.address)
    #Запуск в бэкграунде
    celery_test.delay(db_url._id,'python')
    return redirect('/')
