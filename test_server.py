#!/usr/bin/env python3
"""
Test script for the dummy server API.
"""

import requests
import json
from datetime import datetime


def test_api(base_url="http://127.0.0.1:8000"):
    """Test the dummy server API endpoints."""
    print(f"🧪 Testing Dummy Server API at {base_url}")
    print("=" * 60)
    
    try:
        # Test root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint works")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
        
        print()
        
        # Test health endpoint
        print("2. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint works")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
        
        print()
        
        # Test get all tasks
        print("3. Testing get all tasks...")
        response = requests.get(f"{base_url}/tasks")
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Get tasks works - found {len(tasks)} tasks")
            for task in tasks:
                print(f"   Task {task['id']}: {task['title']} ({task['status']})")
        else:
            print(f"❌ Get tasks failed: {response.status_code}")
        
        print()
        
        # Test create task
        print("4. Testing create task...")
        new_task = {
            "title": "Test API endpoint",
            "description": "This task was created by the test script",
            "assignee": "test@example.com",
            "due_date": "2025-01-30T23:59:59",
            "status": "todo"
        }
        response = requests.post(
            f"{base_url}/tasks",
            json=new_task,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            created_task = response.json()
            print("✅ Create task works")
            print(f"   Created task ID: {created_task['id']}")
            task_id = created_task['id']
        else:
            print(f"❌ Create task failed: {response.status_code}")
            print(f"   Response: {response.text}")
            task_id = None
        
        print()
        
        # Test get specific task
        if task_id:
            print("5. Testing get specific task...")
            response = requests.get(f"{base_url}/tasks/{task_id}")
            if response.status_code == 200:
                task = response.json()
                print("✅ Get specific task works")
                print(f"   Task: {task['title']} - {task['status']}")
            else:
                print(f"❌ Get specific task failed: {response.status_code}")
            
            print()
            
            # Test update task
            print("6. Testing update task...")
            update_data = {
                "status": "in_progress",
                "description": "Updated by test script"
            }
            response = requests.put(
                f"{base_url}/tasks/{task_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                updated_task = response.json()
                print("✅ Update task works")
                print(f"   Updated status: {updated_task['status']}")
            else:
                print(f"❌ Update task failed: {response.status_code}")
            
            print()
            
            # Test delete task
            print("7. Testing delete task...")
            response = requests.delete(f"{base_url}/tasks/{task_id}")
            if response.status_code == 200:
                print("✅ Delete task works")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Delete task failed: {response.status_code}")
        
        print()
        
        # Test filter by status
        print("8. Testing filter by status...")
        response = requests.get(f"{base_url}/tasks?status=todo")
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Filter by status works - found {len(tasks)} todo tasks")
        else:
            print(f"❌ Filter by status failed: {response.status_code}")
        
        print()
        print("🎉 API testing completed!")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to server at {base_url}")
        print("   Make sure the server is running with: python run_server.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the Dummy Server API")
    parser.add_argument(
        "--url",
        type=str,
        default="http://127.0.0.1:8000",
        help="Base URL for the API (default: http://127.0.0.1:8000)"
    )
    
    args = parser.parse_args()
    test_api(args.url)
