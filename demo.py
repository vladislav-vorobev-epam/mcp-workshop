#!/usr/bin/env python3
"""
Demo script showing the Dummy Server capabilities.
"""

import time
import subprocess
import threading
import requests
from datetime import datetime, timedelta


def start_server():
    """Start the server in a subprocess."""
    return subprocess.Popen(
        ["python", "run_server.py", "--port", "8080"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def wait_for_server(url="http://127.0.0.1:8080", timeout=30):
    """Wait for the server to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/health")
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    return False


def demo_api():
    """Demonstrate the API capabilities."""
    base_url = "http://127.0.0.1:8080"
    
    print("🚀 Dummy Server API Demo")
    print("=" * 50)
    
    # Show server info
    print("📡 Server Information:")
    response = requests.get(f"{base_url}/")
    server_info = response.json()
    print(f"   Title: {server_info['title']}")
    print(f"   Version: {server_info['version']}")
    print(f"   Docs: http://127.0.0.1:8080{server_info['docs_url']}")
    print()
    
    # Show initial tasks
    print("📋 Initial Tasks:")
    response = requests.get(f"{base_url}/tasks")
    tasks = response.json()
    for task in tasks:
        print(f"   {task['id']}. {task['title']} [{task['status']}] - {task['assignee']}")
    print()
    
    # Create a new task
    print("✨ Creating a new task...")
    new_task = {
        "title": "Demo Task",
        "description": "This task was created by the demo script",
        "assignee": "demo@example.com",
        "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "status": "todo"
    }
    response = requests.post(f"{base_url}/tasks", json=new_task)
    created_task = response.json()
    task_id = created_task['id']
    print(f"   ✅ Created task {task_id}: {created_task['title']}")
    print()
    
    # Update the task
    print("🔄 Updating the task...")
    update_data = {
        "status": "in_progress",
        "description": "Task updated by demo script - now in progress!"
    }
    response = requests.put(f"{base_url}/tasks/{task_id}", json=update_data)
    updated_task = response.json()
    print(f"   ✅ Updated task {task_id}: status = {updated_task['status']}")
    print()
    
    # Filter tasks by status
    print("🔍 Filtering tasks by status (in_progress):")
    response = requests.get(f"{base_url}/tasks?status=in_progress")
    filtered_tasks = response.json()
    for task in filtered_tasks:
        print(f"   {task['id']}. {task['title']} - {task['assignee']}")
    print()
    
    # Search by assignee
    print("🔍 Searching tasks by assignee (demo@example.com):")
    response = requests.get(f"{base_url}/tasks?assignee=demo@example.com")
    search_results = response.json()
    for task in search_results:
        print(f"   {task['id']}. {task['title']} - due: {task['due_date']}")
    print()
    
    # Show task details
    print(f"📄 Task {task_id} details:")
    response = requests.get(f"{base_url}/tasks/{task_id}")
    task_details = response.json()
    print(f"   Title: {task_details['title']}")
    print(f"   Description: {task_details['description']}")
    print(f"   Assignee: {task_details['assignee']}")
    print(f"   Status: {task_details['status']}")
    print(f"   Due: {task_details['due_date']}")
    print(f"   Created: {task_details['created_at']}")
    print(f"   Updated: {task_details['updated_at']}")
    print()
    
    # Complete the task
    print("✅ Completing the task...")
    response = requests.put(f"{base_url}/tasks/{task_id}", json={"status": "done"})
    completed_task = response.json()
    print(f"   ✅ Task {task_id} marked as {completed_task['status']}")
    print()
    
    # Show final task count
    response = requests.get(f"{base_url}/health")
    health_info = response.json()
    print(f"📊 Total tasks in system: {health_info['total_tasks']}")
    print()
    
    print("🎉 Demo completed! Check out the interactive docs at:")
    print(f"   📚 Swagger UI: http://127.0.0.1:8080/docs")
    print(f"   📖 ReDoc: http://127.0.0.1:8080/redoc")


def main():
    """Main demo function."""
    print("🚀 Starting Dummy Server Demo...")
    
    # Start the server
    print("📡 Starting server on port 8080...")
    server_process = start_server()
    
    try:
        # Wait for server to be ready
        print("⏳ Waiting for server to be ready...")
        if not wait_for_server():
            print("❌ Server failed to start within timeout")
            return
        
        print("✅ Server is ready!")
        print()
        
        # Run the demo
        demo_api()
        
        print("\n⏸️  Server is still running. Press Ctrl+C to stop.")
        
        # Keep the demo running until user interrupts
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Demo stopped by user")
    
    finally:
        # Clean up
        print("🧹 Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("✅ Server stopped")


if __name__ == "__main__":
    main()
