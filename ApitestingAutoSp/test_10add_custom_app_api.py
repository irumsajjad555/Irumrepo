# test_simple_ai_app.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import time
import random
import string
from playwright.sync_api import sync_playwright
from config import BASE_URL, AI_SERVER_URL, ENVIRONMENT_NAME, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
def test_add_single_app():
    """Simple: Add app inside environment"""
    
    with sync_playwright() as p:
        # 1. Login
        req = p.request.new_context(base_url=BASE_URL)
        login = req.post("/api/auth/login",
            data=json.dumps({"username": SUPERADMIN_USERNAME, "password": SUPERADMIN_PASSWORD}),
            headers={"Content-Type": "application/json"})
        
        if login.status != 200:
            print(f"❌ Login failed")
            return
        
        token = login.json()["token"]
        print("✅ Logged in")
        
        # 2. Generate random app name
        timestamp = int(time.time())
        random_id = random.randint(1000, 9999)
        app_name = f"ai_app_{timestamp}_{random_id}"
        
        # 3. Add ONE app (Email Classification)
        payload = {
            "ip": AI_SERVER_URL + "/",
            "appName": app_name,
            "key": "app-DrCRwXL3CWGmxvgJDXeTicjp",
            "env": ENVIRONMENT_NAME
        }
        
        print(f"\n📤 Adding app:")
        print(f"   Name: {app_name}")
        print(f"   Env: {ENVIRONMENT_NAME}")
        print(f"   Server: {AI_SERVER_URL}")
        
        response = req.post(
            f"/aiCenter/env/{ENVIRONMENT_NAME}/insert",
            multipart={
                "data": json.dumps(payload),
                "capabilityType": "CustomApp"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"\n📥 Response:")
        print(f"   Status: {response.status}")
        print(f"   Message: {response.text()}")
        
        if response.status in [200, 304]:
            print(f"\n✅ SUCCESS: App added to {ENVIRONMENT_NAME}")
        else:
            print(f"\n❌ FAILED")

if __name__ == "__main__":
    test_add_single_app()