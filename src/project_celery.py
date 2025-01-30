from celery import Celery

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
