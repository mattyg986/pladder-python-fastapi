from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "purple_ladder_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.agents.recruiter.tasks", 
             "app.agents.processor.tasks",
             "app.agents.matcher.tasks",
             "app.agents.search.tasks"]
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_hijack_root_logger=False,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

if __name__ == "__main__":
    celery_app.start() 