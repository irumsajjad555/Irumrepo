# config.py - ONE PLACE TO CHANGE EVERYTHING
# Put this in your project root folder

# ========== BASE URL ==========
BASE_URL = "http://192.168.1.212:8080"  # Change this once for all tests

# ========== LOGIN CREDENTIALS ==========
SUPERADMIN_USERNAME = "superadmin"
SUPERADMIN_PASSWORD = "Admin@1234"

# ========== ENVIRONMENT SETTINGS ==========
ENVIRONMENT_NAME = "Irumtestenv2"  # Use this everywhere
JENKINS_FOLDER = "Irumtestenv2"    # Same as environment name
PROCESS_TYPE = "attended"

# ========== LICENSES ==========
ATTENDED_LICENSE = "d1b434ba-7990-47bd-9a93-2e6afeeca069"
MULTI_TASKING = "83b0cd36-19f6-4ff3-8b64-7c6db868cc91"
TASKHUB_LICENSE = "c4c1fbdf-1edd-49bb-b101-48d9b4ead773"
PROCESS_LICENSE = ""  # Add if you have

# ========== AI CENTER SETTINGS ==========
AI_SERVER_URL = "http://192.168.1.218"

# ========== TEST FILES ==========
ROBOT_FILE = "approvaltask.robot"
FILE_NAME = "approvaltask"

# ========== DEFAULT HEADERS ==========
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*"
}