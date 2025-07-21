"""
In-memory storage for tasks.
"""

from datetime import datetime
from typing import Dict, List, Optional
from .models import Task, TaskCreate, TaskUpdate


class TaskStorage:
    """In-memory storage for tasks."""
    
    def __init__(self):
        """Initialize the storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
    
    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task."""
        now = datetime.utcnow()
        task = Task(
            id=self._next_id,
            created_at=now,
            updated_at=now,
            **task_data.model_dump()
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self._tasks.values())
    
    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update an existing task."""
        if task_id not in self._tasks:
            return None
        
        task = self._tasks[task_id]
        update_data = task_update.model_dump(exclude_unset=True)
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            for field, value in update_data.items():
                setattr(task, field, value)
        
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def search_tasks(
        self, 
        assignee: Optional[str] = None, 
        status: Optional[str] = None,
        title_contains: Optional[str] = None
    ) -> List[Task]:
        """Search tasks by various criteria."""
        tasks = list(self._tasks.values())
        
        if assignee:
            tasks = [t for t in tasks if t.assignee and assignee.lower() in t.assignee.lower()]
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        if title_contains:
            tasks = [t for t in tasks if title_contains.lower() in t.title.lower()]
        
        return tasks
    
    def get_task_count(self) -> int:
        """Get the total number of tasks."""
        return len(self._tasks)
    
    def clear_all_tasks(self) -> int:
        """Clear all tasks and return the count of deleted tasks."""
        count = len(self._tasks)
        self._tasks.clear()
        self._next_id = 1
        return count
