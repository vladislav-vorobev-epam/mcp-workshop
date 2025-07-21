# Dummy Task Server

A simple FastAPI-based REST API server for managing tasks with full CRUD operations.

## Features

- ✅ **Create, Read, Update, Delete** tasks
- 🔍 **Search and filter** tasks by assignee, status, or title
- 📊 **Status management** (todo, in_progress, done, cancelled)
- 📅 **Due date tracking** with datetime support
- 👤 **Assignee management**
- 🔧 **Configurable server** settings
- 📚 **Auto-generated API documentation** (Swagger UI + ReDoc)
- 🚀 **Hot reload** for development

## Task Model

Each task has the following properties:

- `id`: Unique identifier (auto-generated)
- `title`: Task title (required, 1-200 characters)
- `description`: Task description (optional, max 1000 characters)
- `assignee`: Person assigned to the task (optional, max 100 characters)
- `due_date`: Due date in ISO format (optional)
- `status`: Current status (todo, in_progress, done, cancelled)
- `created_at`: Creation timestamp (auto-generated)
- `updated_at`: Last update timestamp (auto-updated)

## Quick Start

### 1. Install Dependencies

```bash
poetry install
```

### 2. Run the Server

```bash
# Simple start
python run_server.py

# Custom host and port
python run_server.py --host 0.0.0.0 --port 8080

# With auto-reload (development)
python run_server.py --reload

# Production mode
python run_server.py --no-reload --log-level warning
```

### 3. Access the API

- **Server**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **Alternative Documentation**: http://127.0.0.1:8000/redoc

## API Endpoints

### General
- `GET /` - Server information
- `GET /health` - Health check

### Tasks
- `GET /tasks` - Get all tasks (with optional filtering)
- `GET /tasks/{task_id}` - Get specific task
- `POST /tasks` - Create new task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task
- `GET /tasks/status/{status}` - Get tasks by status
- `DELETE /tasks` - Clear all tasks

### Query Parameters for `/tasks`
- `assignee` - Filter by assignee (partial match)
- `status` - Filter by status (exact match)
- `title_contains` - Filter by title content (partial match)

## Usage Examples

### Create a Task

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "Review pull request",
    "description": "Review the new feature implementation",
    "assignee": "reviewer@example.com",
    "due_date": "2025-01-25T17:00:00",
    "status": "todo"
  }'
```

### Get All Tasks

```bash
curl "http://127.0.0.1:8000/tasks"
```

### Filter Tasks

```bash
# By assignee
curl "http://127.0.0.1:8000/tasks?assignee=developer@example.com"

# By status
curl "http://127.0.0.1:8000/tasks?status=in_progress"

# By title content
curl "http://127.0.0.1:8000/tasks?title_contains=documentation"
```

### Update a Task

```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \\
  -H "Content-Type: application/json" \\
  -d '{
    "status": "done",
    "description": "Updated description"
  }'
```

### Delete a Task

```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```

## Configuration

The server can be configured using environment variables or by creating a `.env` file:

```bash
cp .env.example .env
```

Available configuration options:
- `SERVER_HOST` - Server host (default: 127.0.0.1)
- `SERVER_PORT` - Server port (default: 8000)
- `SERVER_RELOAD` - Enable auto-reload (default: true)
- `LOG_LEVEL` - Log level (default: info)
- `API_TITLE` - API title
- `API_DESCRIPTION` - API description
- `API_VERSION` - API version

## Sample Data

The server comes with pre-loaded sample tasks for testing:

1. **Setup development environment** (done)
2. **Implement FastAPI server** (in_progress)
3. **Write documentation** (todo)

## Development

### Project Structure

```
src/dummy_server/
├── __init__.py          # Module exports
├── config.py            # Server configuration
├── models.py            # Pydantic data models
├── server.py            # FastAPI application
└── storage.py           # In-memory task storage
```

### Adding New Features

1. Update models in `models.py` if needed
2. Add new endpoints in `server.py`
3. Update storage logic in `storage.py` if required
4. Test using the interactive docs at `/docs`

## Interactive Testing

The best way to explore the API is through the auto-generated documentation:

1. Start the server: `python run_server.py`
2. Open http://127.0.0.1:8000/docs
3. Use the "Try it out" buttons to test endpoints interactively

The documentation shows:
- Request/response schemas
- Example values
- Parameter descriptions
- Response codes and error messages
