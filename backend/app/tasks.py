from app.worker import celery_app
import logging
import time

logger = logging.getLogger(__name__)

@celery_app.task
def example_task(name):
    """
    An example task that logs a message and returns a greeting.
    """
    logger.info(f"Running example task for {name}")
    # Simulate some work
    time.sleep(2)
    return f"Hello, {name}!"

@celery_app.task
def long_running_task(task_id):
    """
    A longer running example task that updates progress.
    """
    logger.info(f"Starting long running task {task_id}")
    total_steps = 10
    
    for step in range(total_steps):
        # Simulate work
        time.sleep(5)
        progress = (step + 1) / total_steps * 100
        logger.info(f"Task {task_id}: {progress:.1f}% complete")
    
    logger.info(f"Task {task_id} completed")
    return {"task_id": task_id, "status": "completed"} 