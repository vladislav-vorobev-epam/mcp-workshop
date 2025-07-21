# mcp-workshop

A workshop project demonstrating Model Context Protocol (MCP) implementation with a FastAPI dummy server.

## Project Structure

```
mcp-workshop/
├── src/
│   ├── main.py                    # Main application entry point
│   └── dummy_server/              # FastAPI server module
│       ├── __init__.py           # Module exports
│       ├── config.py             # Server configuration
│       ├── models.py             # Pydantic data models
│       ├── server.py             # FastAPI application
│       └── storage.py            # In-memory task storage
├── run_server.py                  # CLI script to run the server
├── test_server.py                 # API testing script
├── DUMMY_SERVER_README.md         # Detailed server documentation
├── .env.example                   # Configuration template
└── pyproject.toml                 # Poetry dependencies
```

## Features

### Dummy Task Server
- ✅ **REST API** with FastAPI
- 🔧 **CRUD operations** for tasks
- 📊 **Task management** with status, assignee, due dates
- 🔍 **Search and filtering** capabilities
- 📚 **Auto-generated documentation** (Swagger UI + ReDoc)
- ⚙️ **Configurable** host, port, and settings

## Quick Start

### 1. Install Dependencies

```bash
poetry install
```

### 2. Run the Dummy Server

```bash
# Start server on default port (8000)
python run_server.py

# Start on custom port
python run_server.py --port 8080

# Start with auto-reload for development
python run_server.py --reload
```

### 3. Access the API

- **Server**: http://127.0.0.1:8000
- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc

### 4. Test the API

```bash
# Run API tests
python test_server.py

# Test with custom URL
python test_server.py --url http://127.0.0.1:8080
```

## API Overview

The dummy server provides a complete REST API for task management:

### Task Model
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation",
  "assignee": "developer@example.com",
  "due_date": "2025-01-30T23:59:59",
  "status": "in_progress",
  "created_at": "2025-01-21T10:00:00",
  "updated_at": "2025-01-21T15:30:00"
}
```

### Available Endpoints
- `GET /` - Server information
- `GET /health` - Health check
- `GET /tasks` - List all tasks (with filtering)
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `GET /tasks/status/{status}` - Filter by status
- `DELETE /tasks` - Clear all tasks

## Configuration

Create a `.env` file for custom configuration:

```bash
cp .env.example .env
```

Available settings:
- `SERVER_HOST` - Server host (default: 127.0.0.1)
- `SERVER_PORT` - Server port (default: 8000)
- `SERVER_RELOAD` - Enable auto-reload (default: true)
- `LOG_LEVEL` - Logging level (default: info)

## Development

### Project Setup
1. Clone the repository
2. Install dependencies: `poetry install`
3. Run the server: `python run_server.py`
4. Open API docs: http://127.0.0.1:8000/docs

### Adding Features
1. Update models in `src/dummy_server/models.py`
2. Add endpoints in `src/dummy_server/server.py`
3. Test using the interactive documentation

## Documentation

- See [DUMMY_SERVER_README.md](./DUMMY_SERVER_README.md) for detailed server documentation
- Interactive API docs available at `/docs` when server is running
- Alternative documentation at `/redoc`

## Dependencies

- **FastAPI** - Modern web framework for APIs
- **Uvicorn** - ASGI server for FastAPI
- **Pydantic** - Data validation and serialization
- **Requests** - HTTP client for testing