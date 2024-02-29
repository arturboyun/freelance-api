from celery import Celery

from app.config import settings

celery_app = Celery("tasks", backend=settings.redis_url, broker=settings.redis_url)


# hearthbeat celery
@celery_app.task()
def celery_hearth_beat():
    print("celery is alive")


celery_app.conf.beat_schedule = {
    "healthcheck": {
        "task": "tasks.main.celery_hearth_beat",
        "schedule": 10.0
    },
}
celery_app.conf.timezone = "UTC"
