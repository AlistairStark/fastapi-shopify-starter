import os

import celery
from celery import Celery

celery = Celery(
    __name__,
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND"),
)


def init_celery(app):
    celery.conf.update(app.config)
    celery.autodiscover_tasks(["app.worker"], force=True)
