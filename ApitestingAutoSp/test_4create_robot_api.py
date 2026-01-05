import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uuid
from playwright.sync_api import sync_playwright
from config import BASE_URL, ENVIRONMENT_NAME, ATTENDED_LICENSE, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
def test_create_robot():
    """Create robot with attended license using URL format"""
    print("🤖 Creating Robot with Attended License")
    
    with sync_playwright() as p:
        # Login
        req = p.request.new_context(base_url=BASE_URL)
        login = req.post("/api/auth/login", 
                        data={"username": SUPERADMIN_USERNAME, "password": SUPERADMIN_PASSWORD})
        token = login.json()["token"]
        
        # Auth request
        auth = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )
        
        # Generate robot name
        robot_name = f"robot{uuid.uuid4().hex[:8]}"
        
        # Create robot using URL format (this works!)
        url = f"/machine/create?name={robot_name}&envName={ENVIRONMENT_NAME}&licenseId={ATTENDED_LICENSE}"
        response = auth.post(url)
        
        print(f"Robot: {robot_name}")
        print(f"Environment: {ENVIRONMENT_NAME}")
        print(f"License: {ATTENDED_LICENSE}")
        print(f"Status: {response.status}")
        print(f"Response: {response.text()}")
        
        if response.status == 200:
            print("✅ Robot created successfully!")
        else:
            print("❌ Robot creation failed")

if __name__ == "__main__":
    test_create_robot()