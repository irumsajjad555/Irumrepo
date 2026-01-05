# test_7create_queue_api.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uuid
import json
from playwright.sync_api import sync_playwright
from config import BASE_URL, ENVIRONMENT_NAME, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD

def test_create_queue():
    print("📊 Creating Queue")
    
    with sync_playwright() as p:
        # Login
        req = p.request.new_context(base_url=BASE_URL)
        login = req.post("/api/auth/login", 
                        data={"username": SUPERADMIN_USERNAME, "password": SUPERADMIN_PASSWORD})
        token = login.json()["token"]
        
        # Setup request
        auth = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json, text/plain, */*"
            }
        )
        
        # Generate queue name
        queue_uuid = uuid.uuid4().hex[:8]
        queue_name = f"queue{queue_uuid}"
        
        # Create payload
        payload = {
            "queueName": queue_name,
            "description": f"Queue {queue_uuid} for testing",
            "environment": ENVIRONMENT_NAME,
            "MaxNoOfRetries": "0",
            "encrypted": 0,
            "id": "",
            "sla": 0,
            "Hdays": "",
            "Hhours": "",
            "Hmints": "",
            "Mdays": "",
            "Mhours": "",
            "Mmints": "",
            "Ldays": "",
            "Lhours": "",
            "Lmints": "",
            "uniqueReference": 0,
            "reference": 0
        }
        
        # Send as form data with "data" field
        response = auth.post(
            f"/queue/env/{ENVIRONMENT_NAME}/create",
            form={"data": json.dumps(payload)}
        )
        
        print(f"Queue Name: {queue_name}")
        print(f"Status: {response.status}")
        print(f"Response: {response.text()}")
        
        if response.status == 200:
            print("✅ Queue created!")
        else:
            print("❌ Queue creation failed")

if __name__ == "__main__":
    test_create_queue()