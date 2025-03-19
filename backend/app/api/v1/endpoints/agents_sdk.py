from typing import Dict, Any
import asyncio

from fastapi import APIRouter, HTTPException, status, BackgroundTasks

from app.services.agents_sdk_service import AgentSDKService

router = APIRouter()
agent_sdk_service = AgentSDKService()

@router.post("/process-candidate")
async def process_candidate(data: Dict[str, Any]):
    """
    Process a candidate using the Agents SDK.
    
    This endpoint allows direct testing of the Agents SDK without going through Celery.
    """
    try:
        candidate_data = data.get("candidate_data", {})
        job_data = data.get("job_data", {})
        
        # Run the Agents SDK processing
        result = await agent_sdk_service.process_candidate(candidate_data, job_data)
        
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing candidate: {str(e)}"
        )

@router.post("/search-candidates")
async def search_candidates(data: Dict[str, Any]):
    """
    Search for candidates using the Agents SDK.
    
    This endpoint allows direct testing of the Agents SDK without going through Celery.
    """
    try:
        job_requirements = data.get("job_requirements", {})
        filters = data.get("filters", {})
        
        # Run the Agents SDK processing
        result = await agent_sdk_service.search_candidates(job_requirements, filters)
        
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching candidates: {str(e)}"
        )

@router.post("/process-task")
async def process_task(data: Dict[str, Any]):
    """
    Process a general task using the Agents SDK with triage agent.
    
    This endpoint allows direct testing of the Agents SDK without going through Celery.
    """
    try:
        task_id = data.get("task_id", f"test-task-{asyncio.current_task().get_name()}")
        action = data.get("action", "process")
        parameters = data.get("parameters", {})
        
        # Run the Agents SDK processing
        result = await agent_sdk_service.process_task(task_id, action, parameters)
        
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing task: {str(e)}"
        ) 