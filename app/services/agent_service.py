import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.agent import Agent, AgentTaskModel
from app.schemas.agent import AgentCreate, AgentResponse, AgentType, AgentStatus, AgentTask, TaskStatus
from app.worker import celery_app


class AgentService:
    """Service for managing agents and their tasks."""
    
    def __init__(self, db: Session = None):
        self.db = next(get_db()) if db is None else db
    
    def create_agent(self, agent_data: AgentCreate) -> AgentResponse:
        """Create a new agent."""
        agent = Agent(
            id=str(uuid.uuid4()),
            name=agent_data.name,
            type=agent_data.type,
            description=agent_data.description,
            status=AgentStatus.ACTIVE,
            parameters=agent_data.parameters or {},
        )
        
        self.db.add(agent)
        self.db.commit()
        self.db.refresh(agent)
        
        return self._agent_to_response(agent)
    
    def get_all_agents(self) -> List[AgentResponse]:
        """Get all agents."""
        agents = self.db.query(Agent).all()
        return [self._agent_to_response(agent) for agent in agents]
    
    def get_agent(self, agent_id: str) -> Optional[AgentResponse]:
        """Get an agent by ID."""
        agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return None
        return self._agent_to_response(agent)
    
    def create_task(self, agent_id: str, task_data: AgentTask, background_tasks: BackgroundTasks = None) -> str:
        """Create a new task for an agent."""
        # Create task in database
        task = AgentTaskModel(
            id=str(uuid.uuid4()),
            agent_id=agent_id,
            action=task_data.action,
            parameters=task_data.parameters,
            priority=task_data.priority,
            status=TaskStatus.QUEUED,
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        # Queue task in Celery
        agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
        if agent:
            task_name = f"app.agents.{agent.type.value}.tasks.{task_data.action}"
            if background_tasks:
                background_tasks.add_task(self._run_task, task_name, task.id, task_data.parameters)
            else:
                celery_task = celery_app.send_task(
                    task_name,
                    args=[task.id],
                    kwargs=task_data.parameters,
                    queue=agent.type.value,
                )
        
        return task.id
    
    def get_task_status(self, agent_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a task."""
        task = self.db.query(AgentTaskModel).filter(
            AgentTaskModel.id == task_id,
            AgentTaskModel.agent_id == agent_id
        ).first()
        
        if not task:
            return None
        
        return task.to_dict()
    
    def _agent_to_response(self, agent: Agent) -> AgentResponse:
        """Convert an agent model to a response schema."""
        return AgentResponse(
            id=agent.id,
            name=agent.name,
            type=agent.type,
            description=agent.description,
            status=agent.status,
            parameters=agent.parameters,
            created_at=agent.created_at,
            updated_at=agent.updated_at,
        )
    
    def _run_task(self, task_name: str, task_id: str, parameters: Dict[str, Any]):
        """Run a task in the background."""
        try:
            # Update task to running state
            task = self.db.query(AgentTaskModel).filter(AgentTaskModel.id == task_id).first()
            if task:
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.utcnow()
                self.db.commit()
            
            # Run the task
            result = celery_app.send_task(task_name, args=[task_id], kwargs=parameters)
            task_result = result.get()  # This will wait for the task to complete
            
            # Update task with result
            task = self.db.query(AgentTaskModel).filter(AgentTaskModel.id == task_id).first()
            if task:
                task.status = TaskStatus.COMPLETED
                task.result = task_result
                task.completed_at = datetime.utcnow()
                self.db.commit()
                
        except Exception as e:
            # Update task with error
            task = self.db.query(AgentTaskModel).filter(AgentTaskModel.id == task_id).first()
            if task:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.completed_at = datetime.utcnow()
                self.db.commit() 