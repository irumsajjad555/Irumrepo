import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uuid
from playwright.sync_api import sync_playwright
from config import BASE_URL, ENVIRONMENT_NAME, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
def test_create_asset():
    """Create asset in Irumtesting using URL format"""
    print("📦 Creating Asset")
    
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
        
        # Generate unique asset name and value
        asset_uuid = uuid.uuid4().hex[:8]
        asset_name = f"asset{asset_uuid}"
        asset_value = f"value{asset_uuid}"
        
        # Create asset using URL parameters
        url = f"/env/{ENVIRONMENT_NAME}/assets/insert?name={asset_name}&value={asset_value}&type=global&environmentName={ENVIRONMENT_NAME}"
        response = auth.post(url)
        
        print(f"Asset Name: {asset_name}")
        print(f"Asset Value: {asset_value}")
        print(f"Type: global")
        print(f"Environment: {ENVIRONMENT_NAME}")
        print(f"Status: {response.status}")
        print(f"Response: {response.text()}")
        
        if response.status == 201:
            print("✅ Asset created successfully!")
        else:
            print("❌ Asset creation failed")

if __name__ == "__main__":
    test_create_asset()