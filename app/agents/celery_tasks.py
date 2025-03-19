"""
Unified Celery tasks for AI agents using the Agents SDK.
Replaces the legacy OpenAI Assistants implementation with the Agents SDK.
"""

import logging
import asyncio
import json
from typing import Dict, Any
from datetime import datetime

from app.worker import celery_app
from app.services.agents_sdk_service import AgentSDKService
from app.schemas.agent import TaskStatus

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

@celery_app.task(name="app.agents.celery_tasks.process_candidate", bind=True)
def process_candidate(self, task_id: str, **kwargs):
    """
    Process a candidate application and provide a summary using the Agents SDK.
    
    Args:
        task_id: The ID of the task
        **kwargs: Task parameters including candidate_data and job_data
    
    Returns:
        Dict with processing result
    """
    logger.info(f"Processing candidate for task {task_id}")
    
    try:
        # Update task status to running using Celery backend
        self.update_state(state=TaskStatus.RUNNING.value, meta={'started_at': datetime.utcnow().isoformat()})
        
        # Get parameters from the task
        candidate_data = kwargs.get("candidate_data", {})
        job_data = kwargs.get("job_data", {})
        
        # Process using Agents SDK
        result = run_async_in_celery(
            agent_sdk_service.process_candidate(candidate_data, job_data)
        )
        
        # Store result in Celery backend
        return {
            'status': TaskStatus.COMPLETED.value,
            'result': result,
            'completed_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing candidate: {str(e)}")
        
        # Update task with error in Celery backend
        error_data = {
            'status': TaskStatus.FAILED.value,
            'error': str(e),
            'completed_at': datetime.utcnow().isoformat()
        }
        self.update_state(state=TaskStatus.FAILED.value, meta=error_data)
        
        raise

@celery_app.task(name="app.agents.celery_tasks.search_candidates", bind=True)
def search_candidates(self, task_id: str, **kwargs):
    """
    Search for candidates matching job requirements using the Agents SDK.
    
    Args:
        task_id: The ID of the task
        **kwargs: Task parameters including job_requirements and filters
    
    Returns:
        Dict with search results
    """
    logger.info(f"Searching candidates for task {task_id}")
    
    try:
        # Update task status to running using Celery backend
        self.update_state(state=TaskStatus.RUNNING.value, meta={'started_at': datetime.utcnow().isoformat()})
        
        # Get parameters from the task
        job_requirements = kwargs.get("job_requirements", {})
        filters = kwargs.get("filters", {})
        
        # Process using Agents SDK
        result = run_async_in_celery(
            agent_sdk_service.search_candidates(job_requirements, filters)
        )
        
        # Store result in Celery backend
        return {
            'status': TaskStatus.COMPLETED.value,
            'result': result,
            'completed_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error searching candidates: {str(e)}")
        
        # Update task with error in Celery backend
        error_data = {
            'status': TaskStatus.FAILED.value,
            'error': str(e),
            'completed_at': datetime.utcnow().isoformat()
        }
        self.update_state(state=TaskStatus.FAILED.value, meta=error_data)
        
        raise

@celery_app.task(name="app.agents.celery_tasks.process_task", bind=True)
def process_task(self, task_id: str, action: str, **kwargs):
    """
    Process a general task using the Agents SDK triage agent.
    
    Args:
        task_id: The ID of the task
        action: The action to perform
        **kwargs: Task parameters
    
    Returns:
        Dict with processing result
    """
    logger.info(f"Processing task {task_id} with action {action}")
    
    try:
        # Update task status to running using Celery backend
        self.update_state(state=TaskStatus.RUNNING.value, meta={'started_at': datetime.utcnow().isoformat()})
        
        # Process using Agents SDK
        result = run_async_in_celery(
            agent_sdk_service.process_task(task_id, action, kwargs)
        )
        
        # Store result in Celery backend
        return {
            'status': TaskStatus.COMPLETED.value,
            'result': result,
            'completed_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing task: {str(e)}")
        
        # Update task with error in Celery backend
        error_data = {
            'status': TaskStatus.FAILED.value,
            'error': str(e),
            'completed_at': datetime.utcnow().isoformat()
        }
        self.update_state(state=TaskStatus.FAILED.value, meta=error_data)
        
        raise 