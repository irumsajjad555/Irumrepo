# test_create_user_api.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from playwright.sync_api import sync_playwright
import uuid
from config import BASE_URL, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD, TASKHUB_LICENSE

def test_create_user():
    """Test user creation via API"""
    with sync_playwright() as p:
        # 1. Login as admin
        req = p.request.new_context(base_url=BASE_URL)
        login_response = req.post(
            "/api/auth/login",
            data={"username": SUPERADMIN_USERNAME, "password": SUPERADMIN_PASSWORD}
        )
        
        assert login_response.status == 200, f"Admin login failed with status {login_response.status}"
        token = login_response.json()["token"]
        
        # 2. Generate unique user data
        unique_id = uuid.uuid4().hex[:8]
        
        payload = {
            "username": f"testuser{unique_id}",
            "password": f"TestPass{unique_id}@",
            "displayName": f"TestUser{unique_id}",
            "email": f"user{unique_id}@example.com",
            "roles": ["Irumtestenv3_admin"],
            "taskhubLicenseId": TASKHUB_LICENSE
        }
        
        # 3. Create user
        auth_req = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*"
            }
        )
        
        create_response = auth_req.post("/api/users", data=payload)
        
        # 4. Verify successful creation
        assert create_response.status == 200, f"User creation failed with status {create_response.status}"
        
        # 5. Verify response contains expected data
        response_data = create_response.json()
        assert response_data is not None, "Response should contain data"
        
        # ONLY show this message
        print("✅ User created successfully!")

if __name__ == "__main__":
    test_create_user()