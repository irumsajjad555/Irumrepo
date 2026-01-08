import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import random
import string
from playwright.sync_api import sync_playwright
from config import BASE_URL, AI_SERVER_URL, ENVIRONMENT_NAME, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD

def test_add_simple_app():
    """Add app with simple number name: app_123, app_456, etc."""
    
    print("\n" + "="*50)
    print("🚀 ADDING SIMPLE APP")
    print("="*50)
    
    # Generate 3 random digits
    random_digits = ''.join(random.choices(string.digits, k=3))
    app_name = f"app_{random_digits}"  # app_123, app_456, app_789
    
    print(f"📱 App Name: {app_name}")
    print(f"🏢 Environment: {ENVIRONMENT_NAME}")
    print(f"🌐 Server: {AI_SERVER_URL}")
    print("-" * 30)
    
    with sync_playwright() as p:
        # 1. Login
        print("🔐 Logging in...")
        req = p.request.new_context(base_url=BASE_URL)
        login = req.post("/api/auth/login",
            data={"username": SUPERADMIN_USERNAME, "password": SUPERADMIN_PASSWORD})
        
        print(f"   Login Status: {login.status}")
        assert login.status == 200, f"Login failed!"
        token = login.json()["token"]
        print("✅ Login successful")
        
        # 2. Add app
        print(f"\n📤 Creating app '{app_name}'...")
        payload = {
            "ip": AI_SERVER_URL + "/",
            "appName": app_name,
            "key": "app-DrCRwXL3CWGmxvgJDXeTicjp",
            "env": ENVIRONMENT_NAME
        }
        
        response = req.post(
            f"/aiCenter/env/{ENVIRONMENT_NAME}/insert",
            multipart={
                "data": json.dumps(payload),
                "capabilityType": "CustomApp"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"📥 Response Status: {response.status}")
        
        if response.status == 200:
            print(f"✅ App '{app_name}' created successfully!")
            try:
                response_json = response.json()
                print(f"📋 Response: {response_json}")
            except:
                print(f"📋 Response: {response.text()[:100]}")
        elif response.status == 304:
            print(f"⚠️ App '{app_name}' already exists")
            # Try once more with different 3 digits
            random_digits = ''.join(random.choices(string.digits, k=3))
            app_name2 = f"app_{random_digits}"
            print(f"🔄 Trying new name: {app_name2}")
            
            payload["appName"] = app_name2
            response2 = req.post(
                f"/aiCenter/env/{ENVIRONMENT_NAME}/insert",
                multipart={
                    "data": json.dumps(payload),
                    "capabilityType": "CustomApp"
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response2.status == 200:
                print(f"✅ App '{app_name2}' created successfully!")
            else:
                print(f"❌ Failed with new name too")
                assert False, f"App creation failed twice!"
        else:
            print(f"❌ App creation failed: {response.status}")
            print(f"📋 Response: {response.text()[:200]}")
            assert False, f"App creation failed!"
        
        print("\n" + "="*50)
        print("✅ TEST COMPLETED")
        print("="*50)

if __name__ == "__main__":
    test_add_simple_app()