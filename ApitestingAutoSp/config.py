# config.py - ONE PLACE TO CHANGE EVERYTHING
# Put this in your project root folder

# ========== BASE URL ==========
BASE_URL = "http://192.168.1.212:8080"  # Change this once for all tests

# ========== LOGIN CREDENTIALS ==========
SUPERADMIN_USERNAME = "superadmin"
SUPERADMIN_PASSWORD = "Admin@1234"

# ========== ENVIRONMENT SETTINGS ==========
ENVIRONMENT_NAME = "Irumtestenv3"  # Use this everywhere
JENKINS_FOLDER = "Irumtestenv3"    # Same as environment name
PROCESS_TYPE = "attended"

# ========== LICENSES ==========
ATTENDED_LICENSE = "7d9f6199-b826-4ae6-804f-345f27f069eb"
MULTI_TASKING = "68e04e79-17c0-42ad-a46a-94fda624ee63"
TASKHUB_LICENSE = "8ac239de-fff4-4f7a-a873-6ca6a268ef80"
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