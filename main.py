# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from celery import Celery
from celery.result import AsyncResult


def make_celery(app):
    celery = Celery('backend.main', backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://',
    CELERY_RESULT_BACKEND='amqp://'
)
celery = make_celery(app)


@celery.task()
def hello(a):
    i = 2
    primfac = []
    while i * i <= n:
        while n % i == 0:
            primfac.append(i)
            n = n / i
        i = i + 1
    if n > 1:
        primfac.append(n)

    	print(n)


@app.route("/run_tasks")
def run_tasks():
    print('Start function')
    tasks = list()
    for i in range(4):
        task = hello.delay(i, i * 2)
        tasks.append(str(task))
    print('End function')
    return jsonify({"tasks": tasks})

@app.route("/check_task/<task_id>")
def check_task(task_id):
    task = hello.AsyncResult(task_id)
    return jsonify({
        "task_id": task.id,
        "result": task.result,
        "state": task.state,
        "ready": task.ready()
    })


if __name__ == "__main__":
app.run(debug=True)
