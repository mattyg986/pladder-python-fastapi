from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime
from app.core.database import Base

# Add created_at and updated_at columns to all models that inherit from Base
class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)