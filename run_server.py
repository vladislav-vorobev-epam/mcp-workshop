#!/usr/bin/env python3
"""
CLI script to run the dummy server.
"""

import argparse
import uvicorn
from src.dummy_server.config import get_server_config


def main():
    """Main entry point for the dummy server CLI."""
    parser = argparse.ArgumentParser(description="Run the Dummy Task Server")
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Host to bind the server (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to bind the server (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["critical", "error", "warning", "info", "debug", "trace"],
        default=None,
        help="Log level (default: info)"
    )
    
    args = parser.parse_args()
    
    # Get configuration
    config = get_server_config()
    
    # Override config with command line arguments
    host = args.host or config.host
    port = args.port or config.port
    log_level = args.log_level or config.log_level
    
    # Handle reload setting
    reload = config.reload
    if args.reload:
        reload = True
    elif args.no_reload:
        reload = False
    
    print(f"🚀 Starting Dummy Task Server...")
    print(f"📍 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"📖 Alternative docs: http://{host}:{port}/redoc")
    print(f"⚙️  Reload enabled: {reload}")
    print(f"📊 Log level: {log_level}")
    print("")
    
    try:
        uvicorn.run(
            "src.dummy_server.server:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
