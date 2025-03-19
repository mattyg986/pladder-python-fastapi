from celery import Celery
import os
import logging

logger = logging.getLogger(__name__)

# Get Redis URL from environment
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Create Celery app
celery_app = Celery('app',
             broker=redis_url,
             backend=redis_url,
             include=['app.tasks'])

# Make app available for backwards compatibility
app = celery_app

# Configure Celery
celery_app.conf.update(
    result_expires=3600,  # 1 hour
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_hijack_root_logger=False,
)

if __name__ == '__main__':
    celery_app.start() 