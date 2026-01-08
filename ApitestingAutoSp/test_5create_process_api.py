import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import time
import os
import random
import string
from playwright.sync_api import sync_playwright
import pytest
from config import BASE_URL, ENVIRONMENT_NAME, JENKINS_FOLDER, PROCESS_TYPE, ROBOT_FILE, FILE_NAME, ATTENDED_LICENSE, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD

# ========== HELPER FUNCTIONS ==========
def generate_random_process_name():
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"process_{random_chars}"

# ========== PROCESS CREATION ==========
def create_process_for_robot(robot_name):
    process_name = generate_random_process_name()
    worker_node = f"{JENKINS_FOLDER}_{robot_name}"
    
    print(f"🏭 Creating Process for Robot: {robot_name}")
    print(f"   Process Name: {process_name}")
    print(f"   Worker Node: {worker_node}")
    
    with sync_playwright() as p:
        # Login
        req = p.request.new_context(base_url=BASE_URL)
        login_response = req.post("/api/auth/login",
            data={"username": SUPERADMIN_USERNAME, "password": SUPERADMIN_PASSWORD})
        
        if login_response.status != 200:
            print(f"❌ Login failed")
            return False
        
        token = login_response.json().get("token")
        
        req_auth = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )
        
        # 1. CREATE JOB
        print(f"   1. Creating job...")
        
        create_response = req_auth.post("/sendPostRequest",
            params={
                "url": f"/job/{JENKINS_FOLDER}/createItem",
                "title": f"creating process {JENKINS_FOLDER} >{process_name}"
            },
            multipart={
                "name": process_name,
                "mode": "hudson.model.FreeStyleProject"
            }
        )
        
        print(f"   Create response: {create_response.status}")
        
        if create_response.status not in [200, 302]:
            print(f"   ❌ Job creation failed")
            return False
        
        print(f"   ✅ Job created")
        time.sleep(3)
        
        # 2. CONFIGURE JOB
        print(f"   2. Configuring job...")
        
        json_payload = '''{"description":"{\\"processType\\":\\"''' + PROCESS_TYPE + '''\\",\\"enableRDA\\":\\"false\\"}","properties":{"stapler-class-bag":"true","jenkins-model-BuildDiscarderProperty":{"specified":false,"":"0","strategy":{"daysToKeepStr":"","numToKeepStr":"","artifactDaysToKeepStr":"","artifactNumToKeepStr":"","stapler-class":"hudson.tasks.LogRotator","$class":"hudson.tasks.LogRotator"}},"com-coravy-hudson-plugins-github-GithubProjectProperty":{},"org-jenkins-plugins-lockableresources-RequiredResourcesProperty":{},"jenkins-branch-RateLimitBranchProperty$JobPropertyImpl":{},"hudson-model-ParametersDefinitionProperty":{"specified":true,"parameterDefinitions":[{"name":"node","defaultSlaves":["''' + worker_node + '''"],"allowedSlaves":["''' + worker_node + '''"],"triggerIfResult":"allowMultiSelectionForConcurrentBuilds","":"0","nodeEligibility":{"stapler-class":"org.jvnet.jenkins.plugins.nodelabelparameter.node.AllNodeEligibility","$class":"org.jvnet.jenkins.plugins.nodelabelparameter.node.AllNodeEligibility"},"description":"","stapler-class":"org.jvnet.jenkins.plugins.nodelabelparameter.NodeParameterDefinition","$class":"org.jvnet.jenkins.plugins.nodelabelparameter.NodeParameterDefinition"}]}},"disable":false,"concurrentBuild":true,"hasSlaveAffinity":true,"label":"''' + worker_node + '''","hasCustomQuietPeriod":false,"quiet_period":"5","hasCustomScmCheckoutRetryCount":false,"scmCheckoutRetryCount":"0","blockBuildWhenUpstreamBuilding":false,"blockBuildWhenDownstreamBuilding":false,"hasCustomWorkspace":false,"customWorkspace":"","displayNameOrNull":"","builder":[{"command":"autosphere --metadata \\"Jenkins Build:$($env:BUILD_NUMBER)\\" --debug debug -d results ''' + FILE_NAME + '''.robot","unstableReturn":"","stapler-class":"hudson.plugins.powershell.PowerShell","$class":"hudson.plugins.powershell.PowerShell"}],"publisher":[{"outputPath":"./results","archiveDirName":"robot-plugin","outputFileName":"output.xml","reportFileName":"report.html","logFileName":"log.html","otherFiles":"","disableArchiveOutput":false,"enableCache":true,"unstableThreshold":"0.0","passThreshold":"0.0","onlyCritical":true,"stapler-class":"hudson.plugins.robot.RobotPublisher","$class":"hudson.plugins.robot.RobotPublisher"},{"buildSteps":{"buildSteps":{"propertiesFilePath":"${WORKSPACE}\\\\results\\\\output.xml","propertiesContent":"","stapler-class":"org.jenkinsci.plugins.envinject.EnvInjectBuilder","$class":"org.jenkinsci.plugins.envinject.EnvInjectBuilder"},"results":["SUCCESS","UNSTABLE","FAILURE","NOT_BUILT","ABORTED"],"stopOnFailure":false,"role":"BOTH"},"markBuildUnstable":false,"stapler-class":"org.jenkinsci.plugins.postbuildscript.PostBuildScript","$class":"org.jenkinsci.plugins.postbuildscript.PostBuildScript"}],"core:apply":"","scm":{"value":"0","stapler-class":"hudson.scm.NullSCM","$class":"hudson.scm.NullSCM"},"hpi-CopyDataToWorkspacePlugin":{"folderPath":"jobs\\\\''' + JENKINS_FOLDER + '''\\\\jobs\\\\''' + process_name + '''\\\\scripts","makeFilesExecutable":false,"deleteFilesAfterBuild":false}}'''
        multipart_data = {
            "json": json_payload,
            "description": '{"processType":"' + PROCESS_TYPE + '","enableRDA":"false"}',
            "allowedSlaves": worker_node,
            "scm": "0",
            "specified": "on",
            "parameter.name": "node", 
            "parameter.description": "",
            "removeme43_triggerIfResult": "allowMultiSelectionForConcurrentBuilds",
            "multiSelectionDisallowed": "",
            "stapler-class": "org.jvnet.jenkins.plugins.nodelabelparameter.node.AllNodeEligibility",
            "$class": "org.jvnet.jenkins.plugins.nodelabelparameter.node.AllNodeEligibility"
        }
        
        config_response = req_auth.post("/sendPostRequest",
            params={
                "url": f"/job/{JENKINS_FOLDER}/job/{process_name}/configSubmit",
                "title": f"updating process {JENKINS_FOLDER}>{process_name}"
            },
            multipart=multipart_data
        )
        
        print(f"   Config response: {config_response.status}")
        
        if config_response.status not in [200, 302]:
            print(f"   ❌ Config failed")
            return False
        
        print(f"   ✅ Configuration applied")
        time.sleep(2)
        
        # 3. UPLOAD PACKAGE - USING EXACT FORMAT FROM MANUAL REQUEST
        print(f"   3. Uploading package...")
        
        if not os.path.exists(ROBOT_FILE):
            print(f"   ❌ Robot file not found: {ROBOT_FILE}")
            return False
        
        # Read file as binary
        with open(ROBOT_FILE, 'rb') as f:
            file_content = f.read()
        
        # EXACT same format as your manual request
        upload_path = f"jobs\\{JENKINS_FOLDER}\\jobs\\{process_name}"
        print(f"   Upload path: {upload_path}")
        print(f"   File size: {len(file_content)} bytes")
        
        # Use Playwright's correct multipart format for binary file
        upload_response = req_auth.post("/processes/uploadPackage",
            multipart={
                "path": upload_path,
                "type": "files",
                "enableRDA": "false",
                "files": {
                    "name": ROBOT_FILE,
                    "mimeType": "application/octet-stream",
                    "buffer": file_content
                }
            }
        )
        
        print(f"   Upload response: {upload_response.status}")
        
        if upload_response.status == 200:
            print(f"   ✅ File uploaded successfully")
            
            # Check response content
            try:
                response_json = upload_response.json()
                print(f"   Upload response data: {response_json}")
            except:
                print(f"   Upload response text: {upload_response.text()[:100]}")
                
        else:
            print(f"   ❌ Upload failed: {upload_response.status}")
            print(f"   Response: {upload_response.text()}")
            
            # Try alternative: send raw bytes without filename dict
            print(f"   Trying alternative format (raw bytes)...")
            upload_response2 = req_auth.post("/processes/uploadPackage",
                multipart={
                    "path": upload_path,
                    "type": "files",
                    "enableRDA": "false",
                    "files": file_content
                }
            )
            
            print(f"   Alternative upload response: {upload_response2.status}")
            print(f"   Alternative response: {upload_response2.text()[:100]}")
            
            if upload_response2.status != 200:
                return False
        
        # ========== SUCCESS ==========
        print(f"   4. Process creation complete...")
        print(f"   🔗 Process URL: {BASE_URL}/job/{JENKINS_FOLDER}/job/{process_name}")
        return True

# ========== NEW ROBOT CREATION (FIXED) ==========
def create_robot(robot_number):
    """Create robot with simple name like myrobot1, myrobot2"""
    robot_name = f"myrobot{robot_number}"
    print(f"🤖 Creating Robot: {robot_name}")
    
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
        
        # Generate robot and environment names
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
        
        print(f"   Environment: {ENVIRONMENT_NAME}")
        print(f"   Robot Name: {robot_name}")
        print(f"   Full Node Name: {env_robot_name}")
        print(f"   Status: {response.status}")
        
        if response.status in [200, 302]:
            print(f"✅ Robot '{robot_name}' created successfully!")
            
            # Also assign license
            assign_license_url = f"/machine/create?name={robot_name}&envName={ENVIRONMENT_NAME}&licenseId={ATTENDED_LICENSE}"
            license_response = auth.post(assign_license_url)
            
            if license_response.status == 200:
                print(f"✅ License assigned to robot '{robot_name}'")
            else:
                print(f"⚠️ Could not assign license: {license_response.status}")
            
            return robot_name
        else:
            print(f"❌ Robot creation failed: {response.text()}")
            return None

# ========== MAIN FLOW ==========
def create_robot_and_process(robot_number):
    print("\n" + "="*60)
    print(f"Creating myrobot{robot_number} with random process")
    print("="*60)
    
    # 1. Create robot with simple name
    robot_name = create_robot(robot_number)
    if not robot_name:
        return False
    
    time.sleep(2)
    
    # 2. Create process for that robot
    success = create_process_for_robot(robot_name)
    
    if success:
        print("="*60)
        print("✅ CREATION COMPLETE")
        print("="*60)
        return True
    else:
        print("="*60)
        print("❌ CREATION FAILED")
        print("="*60)
        return False

# ========== TEST FUNCTION ==========
def test_create_single_robot_process():
    """Test: Create robot1, robot2, robot3... with processes"""
    robot_number = 1  # Start with robot1
    success = create_robot_and_process(robot_number)
    assert success, f"Failed to create myrobot{robot_number}"

if __name__ == "__main__":
    print("🤖 ROBOT & PROCESS CREATION")
    print("="*50)
    
    try:
        robot_number = int(input("Enter robot number (e.g., 1 for myrobot1): ").strip())
        if robot_number >= 1:
            create_robot_and_process(robot_number)
        else:
            print("❌ Invalid number")
    except ValueError:
        print("❌ Invalid input")