# test_logout_api.py (FIXED)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from config import BASE_URL, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD

def test_logout():
    """Simple login and logout test with correct logout endpoint"""
    print("🔐 LOGIN → LOGOUT TEST")
    print("=" * 50)
    print(f"Target: {BASE_URL}\n")
    
    with sync_playwright() as p:
        # 1. LOGIN
        print("📥 STEP 1: LOGIN")
        print("-" * 30)
        
        req = p.request.new_context(base_url=BASE_URL)
        login_response = req.post("/api/auth/login", 
                               data={"username": SUPERADMIN_USERNAME, "password": SUPERADMIN_PASSWORD})
        
        print(f"Endpoint: POST /api/auth/login")
        print(f"Status: {login_response.status}")
        
        # ASSERTION for login
        assert login_response.status == 200, f"Login failed with status {login_response.status}"
        
        token = login_response.json()["token"]
        print(f"✅ Login successful")
        print(f"Token: {token[:30]}...\n")
        
        # 2. LOGOUT
        print("📤 STEP 2: LOGOUT")
        print("-" * 30)
        
        # Create authenticated context
        auth_req = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json, text/plain, */*"
            }
        )
        
        logout_response = auth_req.post("/api/logout")
        
        print(f"Endpoint: POST /api/logout")
        print(f"Status: {logout_response.status}")
        print(f"Expected: 204 No Content")
        
        # ASSERTION for logout
        assert logout_response.status == 204, f"Logout failed with status {logout_response.status}"
        
        print(f"✅ Logout successful (204 No Content)")
        print(f"Response: [No content - as expected]")
        
        # 3. TEST SUMMARY
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("-" * 30)
        print("✅ TEST PASSED Successfully")
        print("✓ Login: 200 OK")
        print("✓ Logout: 204 No Content")
        
        # No return value needed - pytest will know test passed if no assertions fail

if __name__ == "__main__":
    # This allows you to run the script directly too
    test_logout()