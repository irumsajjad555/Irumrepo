# api_tests/tests/test_login_parameterized.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import BASE_URL
import pytest
from playwright.sync_api import sync_playwright

def perform_login(request_context, username, password):
    """Helper function to perform login"""
    login_payload = {
        "username": username,
        "password": password
    }
    return request_context.post(
        "/api/auth/login",
        data=login_payload,
        headers={"Content-Type": "application/json"}
    )

# ---------------------------------------------------------
# Test Data — All scenarios
# ---------------------------------------------------------
login_test_cases = [
    # (username, password, should_pass, description)
    ("superadmin", "Admin@1234", True, "Valid credentials"),
    ("", "", False, "Both empty"),
    ("superadmin", "", False, "Password empty"),
    ("", "Admin@1234", False, "Username empty"),
    ("   ", "   ", False, "Spaces only"),
    ("wronguser", "Admin@1234", False, "Wrong username"),
    ("superadmin", "wrongpass", False, "Wrong password")
]

# ---------------------------------------------------------
# Parameterized Test (runs 7 times!)
# ---------------------------------------------------------
@pytest.mark.parametrize("username, password, should_pass, description", login_test_cases)
def test_login_api(username, password, should_pass, description):
    """Single test that runs for ALL test cases"""
    
    print(f"\n🔍 TEST CASE: {description}")
    print(f"   Username = '{username}', Password = '{password}'")

    with sync_playwright() as p:
        request_context = p.request.new_context(base_url=BASE_URL)
        response = perform_login(request_context, username, password)
        
        print(f"   Status = {response.status}")

        # ----------- EXPECTED TO PASS -----------
        if should_pass:
            assert response.status == 200, "❌ Expected success but got failure!"
            json_data = response.json()
            
            # Must have token for successful login
            assert "token" in json_data, "❌ Token missing in valid login!"
            
            print("✅ PASSED — Valid login returned token!")

        # ----------- EXPECTED TO FAIL -----------
        else:
            assert response.status != 200, "❌ Expected failure but login succeeded!"
            print("✅ Correctly failed — Invalid credentials test passed.")
            # Add this at the VERY END of your test_login.py file
#print("\n🎉 TEST SUMMARY: All 7 login test cases executed successfully!")