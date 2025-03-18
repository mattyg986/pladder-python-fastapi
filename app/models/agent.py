import uuid
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, JSON, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin
from app.schemas.agent import AgentType, AgentStatus, TaskStatus


class Agent(Base, TimestampMixin):
    """Database model for AI Agents."""
    
    __tablename__ = "agent"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    type = Column(Enum(AgentType), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE, nullable=False)
    parameters = Column(JSON, default={})
    
    # Relationships
    tasks = relationship("AgentTaskModel", back_populates="agent", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Agent {self.name} ({self.type.value})>"


class AgentTaskModel(Base, TimestampMixin):
    """Database model for Agent Tasks."""
    
    __tablename__ = "agent_task"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String(36), ForeignKey("agent.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(255), nullable=False)
    parameters = Column(JSON, default={})
    priority = Column(Integer, default=0)
    status = Column(Enum(TaskStatus), default=TaskStatus.QUEUED, nullable=False)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="tasks")
    
    def __repr__(self):
        return f"<AgentTask {self.id} ({self.action}) - {self.status.value}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task model to dictionary."""
        return {
            "task_id": self.id,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }