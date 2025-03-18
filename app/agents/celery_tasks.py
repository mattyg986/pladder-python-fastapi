"""
Unified Celery tasks for AI agents using the Agents SDK.
Replaces the legacy OpenAI Assistants implementation with the Agents SDK.
"""

import logging
import asyncio
from typing import Dict, Any

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.agent import AgentTaskModel, TaskStatus
from app.worker import celery_app
from app.services.agents_sdk_service import AgentSDKService

logger = logging.getLogger(__name__)

# Initialize the Agent SDK service
agent_sdk_service = AgentSDKService()


def run_async_in_celery(coroutine):
    """Helper to run an async function in Celery's synchronous environment."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()


@celery_app.task(name="app.agents.celery_tasks.process_candidate")
def process_candidate(task_id: str, **kwargs):
    """
    Process a candidate application and provide a summary using the Agents SDK.
    
    Args:
        task_id: The ID of the task in the database
        **kwargs: Task parameters including candidate_data and job_data
    
    Returns:
        Dict with processing result
    """
    logger.info(f"Processing candidate for task {task_id}")
    db = next(get_db())
    
    try:
        # Get the task from the database
        task = db.query(AgentTaskModel).filter(AgentTaskModel.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Update task status to running
        task.status = TaskStatus.RUNNING
        db.commit()
        
        # Get parameters from the task
        candidate_data = kwargs.get("candidate_data", {})
        job_data = kwargs.get("job_data", {})
        
        # Process using Agents SDK
        result = run_async_in_celery(
            agent_sdk_service.process_candidate(candidate_data, job_data)
        )
        
        # Update task with result
        task.status = TaskStatus.COMPLETED
        task.result = result
        db.commit()
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing candidate: {str(e)}")
        
        # Update task with error
        task = db.query(AgentTaskModel).filter(AgentTaskModel.id == task_id).first()
        if task:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            db.commit()
        
        raise


@celery_app.task(name="app.agents.celery_tasks.search_candidates")
def search_candidates(task_id: str, **kwargs):
    """
    Search for candidates matching job requirements using the Agents SDK.
    
    Args:
        task_id: The ID of the task in the database
        **kwargs: Task parameters including job_requirements and filters
    
    Returns:
        Dict with search results
    """
    logger.info(f"Searching candidates for task {task_id}")
    db = next(get_db())
    
    try:
        # Get the task from the database
        task = db.query(AgentTaskModel).filter(AgentTaskModel.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Update task status to running
        task.status = TaskStatus.RUNNING
        db.commit()
        
        # Get parameters from the task
        job_requirements = kwargs.get("job_requirements", {})
        filters = kwargs.get("filters", {})
        
        # Process using Agents SDK
        result = run_async_in_celery(
            agent_sdk_service.search_candidates(job_requirements, filters)
        )
        
        # Update task with result
        task.status = TaskStatus.COMPLETED
        task.result = result
        db.commit()
        
        return result
        
    except Exception as e:
        logger.error(f"Error searching candidates: {str(e)}")
        
        # Update task with error
        task = db.query(AgentTaskModel).filter(AgentTaskModel.id == task_id).first()
        if task:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            db.commit()
        
        raise


@celery_app.task(name="app.agents.celery_tasks.process_task")
def process_task(task_id: str, action: str, **kwargs):
    """
    Process a general task using the Agents SDK triage agent.
    
    Args:
        task_id: The ID of the task in the database
        action: The action to perform
        **kwargs: Task parameters
    
    Returns:
        Dict with processing result
    """
    logger.info(f"Processing task {task_id} with action {action}")
    db = next(get_db())
    
    try:
        # Get the task from the database
        task = db.query(AgentTaskModel).filter(AgentTaskModel.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Update task status to running
        task.status = TaskStatus.RUNNING
        db.commit()
        
        # Process using Agents SDK
        result = run_async_in_celery(
            agent_sdk_service.process_task(task_id, action, kwargs)
        )
        
        # Update task with result
        task.status = TaskStatus.COMPLETED
        task.result = result
        db.commit()
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing task: {str(e)}")
        
        # Update task with error
        task = db.query(AgentTaskModel).filter(AgentTaskModel.id == task_id).first()
        if task:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            db.commit()
        
        raise 