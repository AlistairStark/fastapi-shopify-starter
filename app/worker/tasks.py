# from app import models
from app.worker import celery


@celery.task()
def test_task(task_type):
    print("task type", task_type)
    # models.User.query.all()
