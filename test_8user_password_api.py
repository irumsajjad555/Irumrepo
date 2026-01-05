# test_first_login_password_change_api.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from playwright.sync_api import sync_playwright
import uuid
from config import BASE_URL, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD, TASKHUB_LICENSE
def test_first_login_password_change_api():
    """Test password change policy on first login via API"""
    
    with sync_playwright() as p:
        # PART 1: Create a new user
        print("1. Creating new user...")
        
        # Login as superadmin
        req = p.request.new_context(base_url=BASE_URL)
        admin_login = req.post(
            "/api/auth/login",
            data={"username": SUPERADMIN_USERNAME, "password": SUPERADMIN_PASSWORD}
        )
        assert admin_login.status == 200, "Admin login failed"
        admin_token = admin_login.json()["token"]
        
        # Generate unique user data
        unique_id = uuid.uuid4().hex[:8]
        initial_password = f"TempPass{unique_id}@"
        new_password = f"NewPass{unique_id}@123"
        
        user_data = {
            "username": f"newuser{unique_id}",
            "password": initial_password,
            "displayName": f"NewUser{unique_id}",
            "email": f"newuser{unique_id}@example.com",
            "roles": ["Irumtestenv_admin"],
            "taskhubLicenseId": TASKHUB_LICENSE
        }
        
        # Create the user
        auth_req = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        create_response = auth_req.post("/api/users", data=user_data)
        assert create_response.status == 200, f"User creation failed: {create_response.text()}"
        
        # Get the user ID from response (assuming it returns user data)
        user_info = create_response.json()
        user_id = user_info.get("id", user_info.get("userId", 3))  # Default to 3 if not found
        print(f"✅ User created: {user_data['username']} (ID: {user_id})")
        
        # PART 2: First login - should return special response
        print("\n2. First login attempt...")
        
        new_user_req = p.request.new_context(base_url=BASE_URL)
        
        # First login with initial password
        first_login = new_user_req.post(
            "/api/auth/login",
            data={"username": user_data["username"], "password": initial_password}
        )
        
        print(f"   Status: {first_login.status}")
        print(f"   Response: {first_login.text()[:200]}")
        
        # Check if first login works
        if first_login.status == 200:
            first_login_token = first_login.json().get("token")
            print(f"✅ First login successful")
            print(f"   Token: {first_login_token[:30]}...")
        else:
            print(f"❌ First login failed: {first_login.status}")
            print(f"   Full response: {first_login.text()}")
        
        # PART 3: Change password using the correct endpoint
        print("\n3. Changing password...")
        
        # Use the exact endpoint from your network capture
        change_payload = {
            "userId": user_id,
            "password": new_password
        }
        
        # IMPORTANT: Need to be authenticated to change password
        # Use the token from first login
        if first_login.status == 200:
            # Create authenticated context with user's token
            user_auth_req = p.request.new_context(
                base_url=BASE_URL,
                extra_http_headers={
                    "Authorization": f"Bearer {first_login_token}",
                    "Content-Type": "application/json"
                }
            )
            
            # PUT request to change password (as per your network capture)
            change_response = user_auth_req.put(
                f"/api/users/password?userId={user_id}&password={new_password}",
                data=change_payload
            )
            
            print(f"   Endpoint: PUT /api/users/password?userId={user_id}&password={new_password}")
            print(f"   Status: {change_response.status}")
            print(f"   Response: {change_response.text()}")
            
            if change_response.status == 200:
                print("✅ Password changed successfully")
                password_changed = True
            else:
                print(f"❌ Password change failed: {change_response.status}")
                password_changed = False
        else:
            print("⚠️ Cannot change password - first login failed")
            password_changed = False
        
        # PART 4: Verify login with new password
        print("\n4. Verifying login with new password...")
        
        if password_changed:
            # Try login with new password
            second_login = new_user_req.post(
                "/api/auth/login",
                data={"username": user_data["username"], "password": new_password}
            )
            
            print(f"   Status: {second_login.status}")
            
            if second_login.status == 200:
                print("✅ Login successful with new password")
                print("✅ User can now login with changed password")
            else:
                print(f"❌ New password login failed: {second_login.status}")
                print(f"   Response: {second_login.text()}")
        else:
            print("⚠️ Skipping new password login test")
        
if __name__ == "__main__":
    test_first_login_password_change_api()