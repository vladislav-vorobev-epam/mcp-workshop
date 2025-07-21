"""
FastAPI server implementation with CRUD operations for tasks.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse

from .config import get_server_config
from .models import Task, TaskCreate, TaskUpdate, TaskStatus
from .storage import TaskStorage

# Get configuration
config = get_server_config()

# Create FastAPI app
app = FastAPI(
    title=config.title,
    description=config.description,
    version=config.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Create storage instance
task_storage = TaskStorage()

# Add some sample data for demonstration
sample_tasks = [
    TaskCreate(
        title="Setup development environment",
        description="Install Python, Poetry, and VS Code extensions",
        assignee="developer@example.com",
        due_date=datetime(2025, 1, 25, 17, 0, 0),
        status=TaskStatus.DONE
    ),
    TaskCreate(
        title="Implement FastAPI server",
        description="Create a REST API with CRUD operations for tasks",
        assignee="developer@example.com",
        due_date=datetime(2025, 1, 22, 12, 0, 0),
        status=TaskStatus.IN_PROGRESS
    ),
    TaskCreate(
        title="Write documentation",
        description="Document the API endpoints and usage examples",
        assignee="tech-writer@example.com",
        due_date=datetime(2025, 1, 30, 23, 59, 59),
        status=TaskStatus.TODO
    )
]

# Add sample tasks on startup
for sample_task in sample_tasks:
    task_storage.create_task(sample_task)


@app.get("/", summary="Root endpoint", tags=["General"])
async def root():
    """Root endpoint returning server information."""
    return {
        "message": "Welcome to the Dummy Task Server!",
        "title": config.title,
        "version": config.version,
        "docs_url": "/docs",
        "endpoints": {
            "tasks": "/tasks",
            "health": "/health"
        }
    }


@app.get("/health", summary="Health check", tags=["General"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "total_tasks": task_storage.get_task_count()
    }


@app.get("/tasks", response_model=List[Task], summary="Get all tasks", tags=["Tasks"])
async def get_tasks(
    assignee: Optional[str] = Query(None, description="Filter by assignee"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    title_contains: Optional[str] = Query(None, description="Filter by title content")
):
    """
    Get all tasks with optional filtering.
    
    - **assignee**: Filter tasks by assignee (partial match, case-insensitive)
    - **status**: Filter tasks by status
    - **title_contains**: Filter tasks containing text in title (case-insensitive)
    """
    if any([assignee, status, title_contains]):
        return task_storage.search_tasks(
            assignee=assignee,
            status=status.value if status else None,
            title_contains=title_contains
        )
    return task_storage.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=Task, summary="Get a task by ID", tags=["Tasks"])
async def get_task(task_id: int):
    """
    Get a specific task by ID.
    
    - **task_id**: Unique identifier of the task
    """
    task = task_storage.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, summary="Create a new task", tags=["Tasks"])
async def create_task(task: TaskCreate):
    """
    Create a new task.
    
    - **title**: Task title (required, 1-200 characters)
    - **description**: Task description (optional, max 1000 characters)
    - **assignee**: Person assigned to the task (optional, max 100 characters)
    - **due_date**: Due date for the task (optional, ISO format)
    - **status**: Task status (optional, defaults to 'todo')
    """
    created_task = task_storage.create_task(task)
    return created_task


@app.put("/tasks/{task_id}", response_model=Task, summary="Update a task", tags=["Tasks"])
async def update_task(task_id: int, task_update: TaskUpdate):
    """
    Update an existing task.
    
    - **task_id**: Unique identifier of the task
    - All fields are optional and will only update provided values
    """
    updated_task = task_storage.update_task(task_id, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return updated_task


@app.delete("/tasks/{task_id}", summary="Delete a task", tags=["Tasks"])
async def delete_task(task_id: int):
    """
    Delete a task by ID.
    
    - **task_id**: Unique identifier of the task
    """
    deleted = task_storage.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Task {task_id} deleted successfully"}
    )


@app.get("/tasks/status/{status_value}", response_model=List[Task], summary="Get tasks by status", tags=["Tasks"])
async def get_tasks_by_status(status_value: TaskStatus):
    """
    Get all tasks with a specific status.
    
    - **status_value**: Task status (todo, in_progress, done, cancelled)
    """
    return task_storage.search_tasks(status=status_value.value)


@app.delete("/tasks", summary="Clear all tasks", tags=["Tasks"])
async def clear_all_tasks():
    """
    Delete all tasks. Use with caution!
    """
    deleted_count = task_storage.clear_all_tasks()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"All tasks cleared successfully",
            "deleted_count": deleted_count
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.dummy_server.server:app",
        host=config.host,
        port=config.port,
        reload=config.reload,
        log_level=config.log_level
    )
