from app.worker import celery


@celery.task()
def test_task(task_type):
    pass
