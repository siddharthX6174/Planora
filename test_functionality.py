#!/usr/bin/env python3
"""
Comprehensive testing script for Planora application
Tests all main features: auth, tasks, categories, and profile
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api/v1"

# Test user data
TEST_USER = {
    "name": "Test User",
    "email": f"test{datetime.now().timestamp()}@example.com",
    "password": "TestPassword123!"
}

class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
    
    def add_pass(self, test_name):
        self.passed.append(test_name)
        print(f"✓ {test_name}")
    
    def add_fail(self, test_name, error):
        self.failed.append((test_name, error))
        print(f"✗ {test_name}: {error}")
    
    def summary(self):
        total = len(self.passed) + len(self.failed)
        print("\n" + "="*60)
        print(f"Test Summary: {len(self.passed)}/{total} passed")
        print("="*60)
        if self.failed:
            print("\nFailed Tests:")
            for test, error in self.failed:
                print(f"  - {test}: {error}")
        else:
            print("\n✓ All tests passed!")

results = TestResults()
tokens = {}

def test_frontend_routes():
    """Test frontend pages are accessible"""
    print("\n--- Testing Frontend Routes ---")
    
    pages = [
        ("/", "Homepage"),
        ("/register", "Registration page"),
        ("/login", "Login page"),
    ]
    
    for page, name in pages:
        try:
            response = requests.get(f"{BASE_URL}{page}")
            if response.status_code == 200:
                results.add_pass(f"Frontend: {name} loads")
            else:
                results.add_fail(f"Frontend: {name}", f"Status {response.status_code}")
        except Exception as e:
            results.add_fail(f"Frontend: {name}", str(e))

def test_registration():
    """Test user registration"""
    print("\n--- Testing Registration ---")
    
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json=TEST_USER
        )
        if response.status_code == 201:
            data = response.json()
            if 'access_token' in data:
                tokens['access_token'] = data['access_token']
                tokens['refresh_token'] = data.get('refresh_token')
                results.add_pass("User registration successful")
                return True
            else:
                results.add_fail("User registration", "No access token in response")
        else:
            results.add_fail("User registration", f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail("User registration", str(e))
    
    return False

def test_login():
    """Test user login"""
    print("\n--- Testing Login ---")
    
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            }
        )
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                tokens['access_token'] = data['access_token']
                tokens['refresh_token'] = data.get('refresh_token')
                results.add_pass("User login successful")
                return True
            else:
                results.add_fail("User login", "No access token in response")
        else:
            results.add_fail("User login", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("User login", str(e))
    
    return False

def test_dashboard():
    """Test dashboard access"""
    print("\n--- Testing Dashboard ---")
    
    if not tokens.get('access_token'):
        results.add_fail("Dashboard access", "Not logged in")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/dashboard",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        if response.status_code == 200:
            results.add_pass("Dashboard loads successfully")
            return True
        else:
            results.add_fail("Dashboard access", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Dashboard access", str(e))
    
    return False

def test_profile():
    """Test profile page access"""
    print("\n--- Testing Profile ---")
    
    if not tokens.get('access_token'):
        results.add_fail("Profile access", "Not logged in")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/profile",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        if response.status_code == 200:
            results.add_pass("Profile page loads successfully")
            return True
        else:
            results.add_fail("Profile access", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Profile access", str(e))
    
    return False

def test_categories():
    """Test category creation and retrieval"""
    print("\n--- Testing Categories ---")
    
    if not tokens.get('access_token'):
        results.add_fail("Categories", "Not logged in")
        return False
    
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    
    # Get categories
    try:
        response = requests.get(f"{API_URL}/categories", headers=headers)
        if response.status_code == 200:
            results.add_pass("Get categories")
        else:
            results.add_fail("Get categories", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Get categories", str(e))
    
    # Create category
    try:
        response = requests.post(
            f"{API_URL}/categories",
            headers=headers,
            json={"name": "Work", "color": "#FF5733"}
        )
        if response.status_code == 201:
            category_data = response.json()
            tokens['category_id'] = category_data.get('id')
            results.add_pass("Create category")
            return True
        else:
            results.add_fail("Create category", f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail("Create category", str(e))
    
    return False

def test_tasks():
    """Test task creation, retrieval, update, and deletion"""
    print("\n--- Testing Tasks ---")
    
    if not tokens.get('access_token'):
        results.add_fail("Tasks", "Not logged in")
        return False
    
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    task_id = None
    
    # Create task
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "high",
        "status": "todo",
        "due_date": (datetime.now() + timedelta(days=7)).isoformat()
    }
    
    try:
        response = requests.post(
            f"{API_URL}/tasks",
            headers=headers,
            json=task_data
        )
        if response.status_code == 201:
            task = response.json()
            task_id = task.get('id')
            results.add_pass("Create task")
        else:
            results.add_fail("Create task", f"Status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        results.add_fail("Create task", str(e))
        return False
    
    # Get all tasks
    try:
        response = requests.get(f"{API_URL}/tasks", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                results.add_pass("Get all tasks")
            else:
                results.add_fail("Get all tasks", "Invalid response format")
        else:
            results.add_fail("Get all tasks", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Get all tasks", str(e))
    
    # Get single task
    if task_id:
        try:
            response = requests.get(f"{API_URL}/tasks/{task_id}", headers=headers)
            if response.status_code == 200:
                results.add_pass("Get single task")
            else:
                results.add_fail("Get single task", f"Status {response.status_code}")
        except Exception as e:
            results.add_fail("Get single task", str(e))
        
        # Update task
        try:
            response = requests.put(
                f"{API_URL}/tasks/{task_id}",
                headers=headers,
                json={"title": "Updated Test Task", "status": "in_progress"}
            )
            if response.status_code == 200:
                results.add_pass("Update task")
            else:
                results.add_fail("Update task", f"Status {response.status_code}")
        except Exception as e:
            results.add_fail("Update task", str(e))
        
        # Update task status
        try:
            response = requests.patch(
                f"{API_URL}/tasks/{task_id}/status",
                headers=headers,
                json={"status": "done"}
            )
            if response.status_code == 200:
                results.add_pass("Update task status")
            else:
                results.add_fail("Update task status", f"Status {response.status_code}")
        except Exception as e:
            results.add_fail("Update task status", str(e))
        
        # Delete task
        try:
            response = requests.delete(f"{API_URL}/tasks/{task_id}", headers=headers)
            if response.status_code == 204:
                results.add_pass("Delete task")
            else:
                results.add_fail("Delete task", f"Status {response.status_code}")
        except Exception as e:
            results.add_fail("Delete task", str(e))
    
    return True

def test_token_refresh():
    """Test token refresh"""
    print("\n--- Testing Token Refresh ---")
    
    if not tokens.get('refresh_token'):
        results.add_fail("Token refresh", "No refresh token available")
        return False
    
    try:
        response = requests.post(
            f"{API_URL}/auth/refresh",
            json={"refresh_token": tokens['refresh_token']}
        )
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                tokens['access_token'] = data['access_token']
                results.add_pass("Token refresh successful")
                return True
            else:
                results.add_fail("Token refresh", "No new token in response")
        else:
            results.add_fail("Token refresh", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Token refresh", str(e))
    
    return False

def test_user_profile_api():
    """Test user profile API"""
    print("\n--- Testing User Profile API ---")
    
    if not tokens.get('access_token'):
        results.add_fail("User profile API", "Not logged in")
        return False
    
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    
    try:
        response = requests.get(f"{API_URL}/users/profile", headers=headers)
        if response.status_code == 200:
            results.add_pass("Get user profile")
            return True
        else:
            results.add_fail("Get user profile", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Get user profile", str(e))
    
    return False

def main():
    print("="*60)
    print("Planora Application - Comprehensive Functionality Test")
    print("="*60)
    
    # Test frontend
    test_frontend_routes()
    
    # Test authentication
    test_registration()
    test_login()
    
    # Test main features
    test_dashboard()
    test_profile()
    test_categories()
    test_tasks()
    test_user_profile_api()
    test_token_refresh()
    
    # Print summary
    results.summary()

if __name__ == "__main__":
    main()
