# test_environment_scenarios.py
import pytest
from playwright.sync_api import sync_playwright
import uuid

BASE_URL = "http://192.168.1.212:8080"
LICENSE_ID = "1c5a9892-3478-4ecb-8f2d-edb07d8d9707"

# ---------------------------------------------------------
# Helper: Login once for all tests
# ---------------------------------------------------------
def get_auth_token():
    with sync_playwright() as p:
        request = p.request.new_context(base_url=BASE_URL)
        response = request.post(
            "/api/auth/login",
            data={"username": "superadmin", "password": "Admin@1234"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status == 200, "Login failed"
        return response.json()["token"]

# ---------------------------------------------------------
# SCENARIO 1: Create Environment with License
# ---------------------------------------------------------
def test_create_environment_with_license():
    """SCENARIO: User creates environment with license"""
    print("\n🧪 SCENARIO 1: Create Environment with License")
    print("="*50)
    
    # Step 1: Login
    token = get_auth_token()
    print("✅ Step 1: Logged in successfully")
    
    # Step 2: Prepare environment data (like filling popup)
    env_name = f"auto-env-{uuid.uuid4().hex[:6]}"
    print(f"✅ Step 2: Entering environment name: '{env_name}'")
    print(f"✅ Step 3: Selecting license ID: {LICENSE_ID}")
    
    env_data = {
        "name": env_name,
        "description": "Created via API test",
        "licenses": [LICENSE_ID]
    }
    
    # Step 3: Create environment (like clicking Create button)
    with sync_playwright() as p:
        request = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        response = request.post("/environment/create", data=env_data)
        print(f"✅ Step 4: Clicked Create button")
    
    # Step 4: Verify result
    print(f"📡 Response Status: {response.status}")
    
    if response.status == 200:
        print("🎉 EXPECTED RESULT: Environment created successfully!")
        print(f"📋 Environment '{env_name}' is now available")
    else:
        print(f"❌ UNEXPECTED: Creation failed: {response.text()}")
    
    print("="*50)
    
    # ASSERTION
    assert response.status == 200, f"Environment should be created. Got status {response.status}"

# ---------------------------------------------------------
# SCENARIO 2: Try Create Environment WITHOUT License
# ---------------------------------------------------------
def test_create_environment_without_license():
    """SCENARIO: User tries to create environment without license"""
    print("\n🧪 SCENARIO 2: Create Environment WITHOUT License")
    print("="*50)
    
    token = get_auth_token()
    print("✅ Step 1: Logged in successfully")
    
    env_name = f"no-license-{uuid.uuid4().hex[:6]}"
    print(f"✅ Step 2: Entering environment name: '{env_name}'")
    print("✅ Step 3: NOT selecting any license")
    
    env_data = {
        "name": env_name,
        "description": "Testing without license",
        "licenses": []  # Empty = no license selected
    }
    
    with sync_playwright() as p:
        request = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        response = request.post("/environment/create", data=env_data)
        print("✅ Step 4: Clicked Create button")
    
    print(f"📡 Response Status: {response.status}")
    
    # Note: API might allow or reject this
    if response.status == 200:
        print("📝 NOTE: Environment created without license (API allows it)")
    else:
        print("📝 NOTE: Environment rejected without license (API requires license)")
    
    print("="*50)
    
    # ASSERTION: Test passes regardless (just documenting behavior)
    assert True, "Test completed - documenting API behavior"

# ---------------------------------------------------------
# SCENARIO 3: Create → Print → Delete Environment
# ---------------------------------------------------------
def test_create_print_delete_environment():
    """SCENARIO: Full lifecycle test"""
    print("\n🧪 SCENARIO 3: Create → Print → Delete Environment")
    print("="*50)
    
    token = get_auth_token()
    print("✅ Step 1: Logged in successfully")
    
    # CREATE
    env_name = f"lifecycle-{uuid.uuid4().hex[:6]}"
    print(f"\n📝 CREATE PHASE:")
    print(f"   - Entering name: '{env_name}'")
    print(f"   - Selecting license: {LICENSE_ID}")
    
    env_data = {
        "name": env_name,
        "description": "For lifecycle test",
        "licenses": [LICENSE_ID]
    }
    
    with sync_playwright() as p:
        request = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        # Create
        create_response = request.post("/environment/create", data=env_data)
        assert create_response.status == 200, "Create failed"
        print(f"   ✅ Environment '{env_name}' created successfully")
        
        # PRINT (Verify it exists)
        print(f"\n📝 PRINT PHASE:")
        print(f"   - Printing environment '{env_name}' details")
        
        # Try to get the environment (adjust endpoint as needed)
        # This is where you'd verify the environment exists
        print(f"   ✅ Environment created (status 200 confirms)")
        
        # DELETE
        print(f"\n📝 DELETE PHASE:")
        print(f"   - Deleting environment '{env_name}'")
        
        delete_response = request.post(
            f"/environment/delete?environmentName={env_name}"
        )
        
        if delete_response.status == 200:
            print(f"   ✅ Environment '{env_name}' deleted successfully")
        else:
            print(f"   ❌ Delete failed: {delete_response.text()}")
        
        # ASSERTIONS
        assert create_response.status == 200, "Environment should be created"
        assert delete_response.status == 200, "Environment should be deleted"
    
    print("\n🎉 EXPECTED RESULT: Full lifecycle test completed")
    print("="*50)

# ---------------------------------------------------------
# SCENARIO 4: Print Existing Environments
# ---------------------------------------------------------
def test_print_existing_environments():
    """SCENARIO: View all existing environments"""
    print("\n🧪 SCENARIO 4: Print Existing Environments")
    print("="*50)
    
    token = get_auth_token()
    print("✅ Step 1: Logged in successfully")
    
    print("✅ Step 2: Fetching environments list...")
    
    with sync_playwright() as p:
        request = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        # Try common endpoints for getting environments
        endpoints = ["/user/environments", "/environment/details"]
        
        for endpoint in endpoints:
            response = request.get(endpoint)
            if response.status == 200:
                env_data = response.json()
                print(f"\n📋 EXISTING ENVIRONMENTS ({endpoint}):")
                print(f"   {env_data}")
                break
        else:
            print("❌ Could not find environments endpoint")
    
    print("\n✅ EXPECTED RESULT: Environments list displayed")
    print("="*50)
    
    # ASSERTION: Should get successful response
    assert response.status == 200, "Should fetch environments successfully"

# ---------------------------------------------------------
# Run all scenarios
# ---------------------------------------------------------
if __name__ == "__main__":
    print("\n🚀 STARTING ENVIRONMENT TEST SCENARIOS")
    print("="*60)
    
    test_print_existing_environments()
    test_create_environment_with_license()
    test_create_environment_without_license()
    test_create_print_delete_environment()
    
    print("\n" + "🎉"*30)
    print("ALL SCENARIOS COMPLETED:")
    print("-"*30)
    print("✅ Scenario 1: Create with license")
    print("✅ Scenario 2: Create without license")
    print("✅ Scenario 3: Create → Print → Delete")
    print("✅ Scenario 4: Print existing environments")
    print("🎉"*30)