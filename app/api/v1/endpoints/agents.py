from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Path, Depends, status

from app.schemas.agent import (
    AgentCreate, 
    AgentResponse, 
    AgentType, 
    AgentStatus, 
    AgentTask,
    AgentTaskResponse
)
from app.services.agent_service import AgentService

router = APIRouter()
agent_service = AgentService()

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(agent: AgentCreate):
    """
    Create a new AI agent.
    """
    return agent_service.create_agent(agent)

@router.get("/", response_model=List[AgentResponse])
async def list_agents():
    """
    List all AI agents.
    """
    return agent_service.get_all_agents()

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str = Path(..., description="The ID of the agent to get")):
    """
    Get a specific AI agent by ID.
    """
    agent = agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID {agent_id} not found"
        )
    return agent

@router.post("/{agent_id}/tasks", response_model=AgentTaskResponse)
async def create_agent_task(
    agent_id: str = Path(..., description="The ID of the agent to run the task"),
    task: AgentTask = ...,
    background_tasks: BackgroundTasks = None
):
    """
    Create a new task for an agent to execute.
    """
    agent = agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID {agent_id} not found"
        )
    
    task_id = agent_service.create_task(agent_id, task, background_tasks)
    return {"task_id": task_id, "status": "queued"}

@router.get("/{agent_id}/tasks/{task_id}", response_model=AgentTaskResponse)
async def get_agent_task_status(
    agent_id: str = Path(..., description="The ID of the agent"),
    task_id: str = Path(..., description="The ID of the task")
):
    """
    Get the status of a specific agent task.
    """
    task_status = agent_service.get_task_status(agent_id, task_id)
    if not task_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} for agent {agent_id} not found"
        )
    return task_status 