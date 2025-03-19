import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import BackgroundTasks, Depends

from app.core.supabase_client import get_supabase
from app.schemas.agent import AgentCreate, AgentResponse, AgentType, AgentStatus, AgentTask, TaskStatus
from app.worker import celery_app


class AgentService:
    """Service for managing agents and their tasks using Supabase."""
    
    def __init__(self):
        self.supabase = get_supabase()
    
    def create_agent(self, agent_data: AgentCreate) -> AgentResponse:
        """Create a new agent."""
        agent_id = str(uuid.uuid4())
        agent_dict = {
            "id": agent_id,
            "name": agent_data.name,
            "type": agent_data.type.value,
            "description": agent_data.description,
            "status": AgentStatus.ACTIVE.value,
            "parameters": agent_data.parameters or {},
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Insert into Supabase
        result = self.supabase.table('agents').insert(agent_dict).execute()
        if result.data:
            return self._dict_to_agent_response(result.data[0])
        
        # If no data returned, fetch the agent by ID
        get_result = self.supabase.table('agents').select('*').eq('id', agent_id).execute()
        if get_result.data:
            return self._dict_to_agent_response(get_result.data[0])
        
        # Fallback to returning a response with the data we have
        return AgentResponse(
            id=agent_id,
            name=agent_data.name,
            type=agent_data.type,
            description=agent_data.description,
            status=AgentStatus.ACTIVE,
            parameters=agent_data.parameters or {},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    
    def get_all_agents(self) -> List[AgentResponse]:
        """Get all agents."""
        result = self.supabase.table('agents').select('*').execute()
        return [self._dict_to_agent_response(agent) for agent in result.data]
    
    def get_agent(self, agent_id: str) -> Optional[AgentResponse]:
        """Get an agent by ID."""
        result = self.supabase.table('agents').select('*').eq('id', agent_id).execute()
        if not result.data:
            return None
        return self._dict_to_agent_response(result.data[0])
    
    def create_task(self, agent_id: str, task_data: AgentTask, background_tasks: BackgroundTasks = None) -> str:
        """Create a new task for an agent."""
        task_id = str(uuid.uuid4())
        
        # Create task in Supabase
        task_dict = {
            "id": task_id,
            "agent_id": agent_id,
            "action": task_data.action,
            "parameters": task_data.parameters,
            "priority": task_data.priority,
            "status": TaskStatus.QUEUED.value,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Insert into Supabase
        self.supabase.table('agent_tasks').insert(task_dict).execute()
        
        # Map action to the appropriate unified task
        task_mapping = {
            "process_candidate": "app.agents.celery_tasks.process_candidate",
            "search_candidates": "app.agents.celery_tasks.search_candidates",
            # Add any other action mappings here
        }
        
        # Get the task name from mapping or use the process_task fallback
        if task_data.action in task_mapping:
            task_name = task_mapping[task_data.action]
            # Queue task in Celery
            if background_tasks:
                background_tasks.add_task(self._run_task, task_name, task_id, task_data.parameters)
            else:
                celery_app.send_task(
                    task_name,
                    args=[task_id],
                    kwargs=task_data.parameters
                )
        else:
            # Use the generic process_task for other actions
            task_name = "app.agents.celery_tasks.process_task"
            if background_tasks:
                background_tasks.add_task(
                    self._run_task, 
                    task_name, 
                    task_id, 
                    {"action": task_data.action, **task_data.parameters}
                )
            else:
                celery_app.send_task(
                    task_name,
                    args=[task_id, task_data.action],
                    kwargs=task_data.parameters
                )
        
        return task_id
    
    def get_task_status(self, agent_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a task."""
        result = self.supabase.table('agent_tasks').select('*').eq('id', task_id).eq('agent_id', agent_id).execute()
        
        if not result.data:
            return None
        
        task = result.data[0]
        return {
            "task_id": task["id"],
            "agent_id": task["agent_id"],
            "status": task["status"],
            "result": task.get("result", None),
            "error": task.get("error", None),
            "created_at": task.get("created_at", None),
            "started_at": task.get("started_at", None),
            "completed_at": task.get("completed_at", None)
        }
    
    def update_task_status(self, task_id: str, status: TaskStatus, result: Dict[str, Any] = None, error: str = None) -> bool:
        """Update the status of a task."""
        update_dict = {
            "status": status.value,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        if result:
            update_dict["result"] = result
            
        if error:
            update_dict["error"] = error
            
        if status == TaskStatus.RUNNING:
            update_dict["started_at"] = datetime.utcnow().isoformat()
            
        if status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            update_dict["completed_at"] = datetime.utcnow().isoformat()
        
        # Update in Supabase
        result = self.supabase.table('agent_tasks').update(update_dict).eq('id', task_id).execute()
        return len(result.data) > 0
    
    def _dict_to_agent_response(self, agent_dict: Dict[str, Any]) -> AgentResponse:
        """Convert an agent dictionary to a response schema."""
        try:
            # Parse timestamps if they're strings
            created_at = agent_dict.get("created_at")
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            updated_at = agent_dict.get("updated_at")
            if isinstance(updated_at, str):
                updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            
            # Convert string enum values to enum types
            agent_type = agent_dict.get("type")
            if isinstance(agent_type, str):
                agent_type = AgentType(agent_type)
            
            agent_status = agent_dict.get("status")
            if isinstance(agent_status, str):
                agent_status = AgentStatus(agent_status)
            
            return AgentResponse(
                id=agent_dict.get("id"),
                name=agent_dict.get("name"),
                type=agent_type,
                description=agent_dict.get("description"),
                status=agent_status,
                parameters=agent_dict.get("parameters", {}),
                created_at=created_at,
                updated_at=updated_at,
            )
        except Exception as e:
            # Fallback for any conversion errors
            return AgentResponse(
                id=agent_dict.get("id", ""),
                name=agent_dict.get("name", ""),
                type=AgentType.RECRUITER if agent_dict.get("type") is None else agent_dict.get("type"),
                description=agent_dict.get("description", ""),
                status=AgentStatus.ACTIVE if agent_dict.get("status") is None else agent_dict.get("status"),
                parameters=agent_dict.get("parameters", {}),
                created_at=datetime.utcnow() if agent_dict.get("created_at") is None else agent_dict.get("created_at"),
                updated_at=datetime.utcnow() if agent_dict.get("updated_at") is None else agent_dict.get("updated_at"),
            )
    
    def _run_task(self, task_name: str, task_id: str, parameters: Dict[str, Any]):
        """Run a task in the background."""
        try:
            # Update task to running state
            self.update_task_status(task_id, TaskStatus.RUNNING)
            
            # Run the task
            if task_name == "app.agents.celery_tasks.process_task" and "action" in parameters:
                # Handle process_task differently since it needs action as a positional argument
                action = parameters.pop("action")
                result = celery_app.send_task(task_name, args=[task_id, action], kwargs=parameters)
            else:
                # Standard task
                result = celery_app.send_task(task_name, args=[task_id], kwargs=parameters)
                
            task_result = result.get()  # This will wait for the task to complete
            
            # Update task with result
            self.update_task_status(task_id, TaskStatus.COMPLETED, result=task_result)
                
        except Exception as e:
            # Update task with error
            self.update_task_status(task_id, TaskStatus.FAILED, error=str(e)) 