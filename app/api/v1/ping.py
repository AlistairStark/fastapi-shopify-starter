from fastapi import APIRouter

from app.worker import tasks

router = APIRouter()


@router.get("/ping")
def ping_test():
    return {"message": "pong"}


@router.get("/ping-worker")
def ping_worker_test():
    tasks.test_task.delay("ping")
    return {"message": "celery pong"}
