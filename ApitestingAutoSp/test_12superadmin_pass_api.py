# test_superadmin_password_simple.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from playwright.sync_api import sync_playwright
from config import BASE_URL

def test_superadmin_password_simple():
    """Simple Superadmin password update test"""
    
    CURRENT_PASSWORD = "Admin@12345"  # Current password
    NEW_PASSWORD = "Admin@123"       # New password
    
    print(f"Current password: {CURRENT_PASSWORD}")
    print(f"New password: {NEW_PASSWORD}")
    
    with sync_playwright() as p:
        # 1. Login with current password
        req = p.request.new_context(base_url=BASE_URL)
        login_response = req.post(
            "/api/auth/login",
            data={"username": "superadmin", "password": CURRENT_PASSWORD}
        )
        
        assert login_response.status == 200, f"Login failed: {login_response.status}"
        token = login_response.json()["token"]
        print("✅ Login successful")
        
        # 2. Update password
        auth_req = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        payload = {
            "userId": "1",
            "displayName": "superadmin",
            "email": "admin@autosphere.com",
            "active": True,
            "environmentName": "",
            "password": NEW_PASSWORD
        }
        
        update_response = auth_req.put("/api/users", data=payload)
        
        print(f"Update status: {update_response.status}")
        print(f"Update response: {update_response.text()}")
        
        # Assert password updated successfully
        assert update_response.status == 200, f"Password update failed: {update_response.status}"
        print("✅ Password updated successfully")
        
        # 3. Verify new password works
        verify_req = p.request.new_context(base_url=BASE_URL)
        verify_response = verify_req.post(
            "/api/auth/login",
            data={"username": "superadmin", "password": NEW_PASSWORD}
        )
        
        assert verify_response.status == 200, f"New password verification failed: {verify_response.status}"
        print("✅ New password verified successfully")

if __name__ == "__main__":
    test_superadmin_password_simple()
    print("✅ Test completed")