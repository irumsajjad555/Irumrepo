# test_2environment_api.py
from playwright.sync_api import sync_playwright
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest 
from config import BASE_URL, ATTENDED_LICENSE, MULTI_TASKING ,ENVIRONMENT_NAME, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD

def test_create_environment():
    """Create environment if it doesn't exist, otherwise use existing"""
    print(f"🔍 Checking for environment: '{ENVIRONMENT_NAME}'")
    
    with sync_playwright() as p:
        # 1. Login
        request = p.request.new_context(base_url=BASE_URL)
        login = request.post("/api/auth/login", 
                            data={"username": SUPERADMIN_USERNAME, "password": SUPERADMIN_PASSWORD})
        token = login.json()["token"]
        
        # 2. Setup authenticated request
        auth_request = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )
        
        # 3. Check if environment exists
        env_response = auth_request.get("/environment/getAll")
        environment_exists = False
        
        if env_response.status == 200:
            environments = env_response.json()
            for env in environments:
                if env.get("name") == ENVIRONMENT_NAME:
                    environment_exists = True
                    print(f"✅ '{ENVIRONMENT_NAME}' already exists in the system")
                    break
        
        # 4. Create environment only if it doesn't exist
        if not environment_exists:
            print(f"🔄 '{ENVIRONMENT_NAME}' not found, creating...")
            
            # FIX: Use exact payload structure from manual test
            payload = {
                "name": ENVIRONMENT_NAME,
                "description": "",  # Empty string as shown in manual test
                "licenses": [ATTENDED_LICENSE,MULTI_TASKING ]  # Use your license variable
            }
            
            response = auth_request.post("/environment/create", data=payload)
            
            status = response.status
            print(f"Status: {status}")
            print(f"Response: {response.text()}")
            
            if status == 200:
                print(f"✅ '{ENVIRONMENT_NAME}' created successfully!")
            else:
                print(f"❌ Failed to create '{ENVIRONMENT_NAME}'")
        else:
            print(f"✅ Using existing '{ENVIRONMENT_NAME}' environment")

# Run the test
if __name__ == "__main__":
    test_create_environment()