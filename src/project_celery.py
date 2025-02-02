from celery import Celery
from celery.schedules import crontab

from src.config import redis_settings

redis_url = (
    f"redis://{redis_settings.REDIS_HOST}:{redis_settings.REDIS_PORT}/0"
)
celery_app = Celery(
    "tasks",
    broker=redis_url,
    backend=redis_url,
    include=["src.tasks"],
)

celery_app.conf.update(task_track_started=True)
celery_app.conf.beat_schedule = {
    "update_sending_status_for_notifications": {
        "task": "src.tasks.update_sending_status_for_notifications",
        "schedule": crontab(minute="*/1"),
    },
}
