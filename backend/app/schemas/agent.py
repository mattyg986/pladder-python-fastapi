from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class AgentType(str, Enum):
    RECRUITER = "recruiter"
    PROCESSOR = "processor"
    MATCHER = "matcher"
    SEARCH = "search"


class AgentStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


class AgentCreate(BaseModel):
    name: str = Field(..., description="Name of the agent")
    type: AgentType = Field(..., description="Type of agent")
    description: Optional[str] = Field(None, description="Description of the agent's purpose")
    parameters: Optional[Dict[str, Any]] = Field(
        default={}, description="Configuration parameters for the agent"
    )


class AgentResponse(BaseModel):
    id: str = Field(..., description="Unique identifier of the agent")
    name: str = Field(..., description="Name of the agent")
    type: AgentType = Field(..., description="Type of agent")
    description: Optional[str] = Field(None, description="Description of the agent's purpose")
    status: AgentStatus = Field(..., description="Current status of the agent")
    parameters: Dict[str, Any] = Field(
        default={}, description="Configuration parameters for the agent"
    )
    created_at: datetime = Field(..., description="Time when the agent was created")
    updated_at: Optional[datetime] = Field(None, description="Time when the agent was last updated")


class AgentTask(BaseModel):
    action: str = Field(..., description="Action to be performed by the agent")
    parameters: Dict[str, Any] = Field(
        default={}, description="Parameters for the task"
    )
    priority: int = Field(default=0, description="Priority of the task (higher number = higher priority)")


class TaskStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentTaskResponse(BaseModel):
    task_id: str = Field(..., description="Unique identifier of the task")
    status: TaskStatus = Field(..., description="Current status of the task")
    result: Optional[Dict[str, Any]] = Field(None, description="Result of the task execution")
    error: Optional[str] = Field(None, description="Error message if task failed")
    created_at: Optional[datetime] = Field(None, description="Time when the task was created")
    started_at: Optional[datetime] = Field(None, description="Time when the task execution started")
    completed_at: Optional[datetime] = Field(None, description="Time when the task execution completed") 