"""
Data models for the dummy server using Pydantic.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskBase(BaseModel):
    """Base task model with common fields."""
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Task description", max_length=1000)
    assignee: Optional[str] = Field(None, description="Person assigned to the task", max_length=100)
    due_date: Optional[datetime] = Field(None, description="Due date for the task")
    status: TaskStatus = Field(TaskStatus.TODO, description="Current status of the task")


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Model for updating an existing task. All fields are optional."""
    title: Optional[str] = Field(None, description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Task description", max_length=1000)
    assignee: Optional[str] = Field(None, description="Person assigned to the task", max_length=100)
    due_date: Optional[datetime] = Field(None, description="Due date for the task")
    status: Optional[TaskStatus] = Field(None, description="Current status of the task")


class Task(TaskBase):
    """Complete task model with all fields including ID and timestamps."""
    id: int = Field(..., description="Unique task identifier")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the MCP workshop project",
                "assignee": "john.doe@example.com",
                "due_date": "2025-01-30T23:59:59",
                "status": "in_progress",
                "created_at": "2025-01-21T10:00:00",
                "updated_at": "2025-01-21T15:30:00"
            }
        }
