"""
Dummy Server Module

A simple FastAPI server that implements CRUD operations for tasks.
"""

from .models import Task, TaskCreate, TaskUpdate, TaskStatus
from .server import app
from .config import get_server_config
from .storage import TaskStorage

__all__ = ["Task", "TaskCreate", "TaskUpdate", "TaskStatus", "app", "get_server_config", "TaskStorage"]
