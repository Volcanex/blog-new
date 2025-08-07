#!/usr/bin/env python3
"""
Quick test script to demonstrate the API functionality.
Run this after starting flask_server.py to test the endpoints.
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:5000"

def test_api():
    """Test the various API endpoints"""
    print("Testing Blog API endpoints...")
    print("=" * 50)
    
    try:
        # Test health check
        print("1. Health Check:")
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Test pages list
        print("2. Pages List:")
        response = requests.get(f"{BASE_URL}/api/pages")
        print(f"   Status: {response.status_code}")
        pages_data = response.json()
        print(f"   Found {len(pages_data['pages'])} pages:")
        for page in pages_data['pages']:
            print(f"     - {page['title']} ({page['slug']})")
        print()
        
        # Test page-specific endpoints
        print("3. Page-specific endpoints:")
        
        # Test first-post endpoints
        print("   First Post - Hello:")
        response = requests.get(f"{BASE_URL}/api/first-post/hello")
        print(f"     Status: {response.status_code}")
        print(f"     Response: {json.dumps(response.json(), indent=2)}")
        
        # Test tech-setup endpoints
        print("   Tech Setup - Tools:")
        response = requests.get(f"{BASE_URL}/api/tech-setup/tools")
        print(f"     Status: {response.status_code}")
        print(f"     Response: {json.dumps(response.json(), indent=2)}")
        
        # Test travel-memories endpoints
        print("   Travel Memories - Locations:")
        response = requests.get(f"{BASE_URL}/api/travel-memories/locations")
        print(f"     Status: {response.status_code}")
        print(f"     Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Test database functionality
        print("4. Testing database (comments):")
        
        # Post a comment
        comment_data = {
            "comment": "This is a test comment!",
            "timestamp": "2025-01-15T10:30:00Z"
        }
        response = requests.post(f"{BASE_URL}/api/first-post/comments", 
                               json=comment_data)
        print(f"   POST comment status: {response.status_code}")
        
        # Get comments
        response = requests.get(f"{BASE_URL}/api/first-post/comments")
        print(f"   GET comments status: {response.status_code}")
        print(f"   Comments: {json.dumps(response.json(), indent=2)}")
        
        print("\n" + "=" * 50)
        print("API test completed successfully!")
        
    except requests.ConnectionError:
        print("Error: Could not connect to the Flask server.")
        print("Make sure to run 'python3 flask_server.py' first.")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    test_api()