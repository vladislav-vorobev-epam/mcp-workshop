"""
Configuration for the dummy server.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    """Server configuration."""
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port", ge=1, le=65535)
    reload: bool = Field(default=True, description="Enable auto-reload in development")
    log_level: str = Field(default="info", description="Log level")
    title: str = Field(default="Dummy Task Server", description="API title")
    description: str = Field(
        default="A simple FastAPI server for managing tasks with CRUD operations",
        description="API description"
    )
    version: str = Field(default="1.0.0", description="API version")


def get_server_config() -> ServerConfig:
    """Get server configuration from environment variables or defaults."""
    return ServerConfig(
        host=os.getenv("SERVER_HOST", "127.0.0.1"),
        port=int(os.getenv("SERVER_PORT", "8000")),
        reload=os.getenv("SERVER_RELOAD", "true").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info"),
        title=os.getenv("API_TITLE", "Dummy Task Server"),
        description=os.getenv("API_DESCRIPTION", "A simple FastAPI server for managing tasks with CRUD operations"),
        version=os.getenv("API_VERSION", "1.0.0")
    )
