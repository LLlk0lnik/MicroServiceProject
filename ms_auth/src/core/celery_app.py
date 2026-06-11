from celery import Celery
from src.config import settings

celery_app = Celery("ms_auth")
celery_app.conf.broker_url = settings.CELERY_BROKER_URL

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=15 * 60,
)

celery_app.autodiscover_tasks(["src.core.task"])
