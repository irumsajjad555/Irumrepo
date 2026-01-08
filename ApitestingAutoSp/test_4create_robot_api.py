import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uuid
import json
from playwright.sync_api import sync_playwright
from config import BASE_URL, ENVIRONMENT_NAME, ATTENDED_LICENSE, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD

def test_create_robot_with_details():
    """Create robot with proper configuration to avoid blank UI"""
    print("🤖 Creating Robot with Full Configuration")
    
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
        robot_uuid = uuid.uuid4().hex[:8]
        robot_name = f"robot{robot_uuid}"
        env_robot_name = f"{ENVIRONMENT_NAME}_{robot_name}"
        
        # Create JSON payload as per DevOps instructions
        payload = {
            "name": env_robot_name,
            "nodeDescription": json.dumps({
                "environment": ENVIRONMENT_NAME,
                "robot": {},
                "description": ""
            }),
            "remoteFS": "C:/",
            "labelString": f"{robot_name} processTrayMonitoring:false {env_robot_name}:{robot_name}",
            "nodeProperties": {
                "stapler-class-bag": "true",
                "hudson-slaves-EnvironmentVariablesNodeProperty": {
                    "env": []
                },
                "hudson-tools-ToolLocationNodeProperty": {
                    "locations": {
                        "key": "hudson.plugins.git.GitTool$DescriptorImpl@Default",
                        "home": ""
                    }
                }
            },
            "launcher": {
                "stapler-class": "hudson.slaves.JNLPLauncher",
                "$class": "hudson.slaves.JNLPLauncher",
                "workDirSettings": {
                    "disabled": True,
                    "workDirPath": "",
                    "internalDir": "remoting",
                    "failIfWorkDirIsMissing": False
                },
                "webSocket": True,
                "tunnel": "",
                "vmargs": ""
            }
        }
        
        # Send request as form-data
        response = auth.post(
            "/sendPostRequest",
            params={
                "url": f"/computer/doCreateItem?name={env_robot_name}",
                "type": "hudson.slaves.DumbSlave",
                "title": f"creating new robot {env_robot_name}"
            },
            multipart={
                "json": json.dumps(payload)
            }
        )
        
        print(f"Environment: {ENVIRONMENT_NAME}")
        print(f"Robot Name: {robot_name}")
        print(f"Full Node Name: {env_robot_name}")
        print(f"Status: {response.status}")
        print(f"Response: {response.text()}")
        
        if response.status in [200, 302]:
            print("✅ Robot created successfully with full configuration!")
            
            # Also need to assign license (optional but recommended)
            assign_license_url = f"/machine/create?name={robot_name}&envName={ENVIRONMENT_NAME}&licenseId={ATTENDED_LICENSE}"
            license_response = auth.post(assign_license_url)
            
            if license_response.status == 200:
                print("✅ License assigned to robot")
            else:
                print(f"⚠️ Could not assign license: {license_response.status}")
                
        else:
            print("❌ Robot creation failed")

if __name__ == "__main__":
    test_create_robot_with_details()