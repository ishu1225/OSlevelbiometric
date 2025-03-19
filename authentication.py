import sys
import os
import ctypes
from ctypes import wintypes
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMessageBox

USER_FILE = "registered_user.txt"  # File storing registered user
LOG_FILE = "auth_log.txt"  # Log file for authentication attempts

def get_current_user():
    """ Get the current Windows username """
    buffer_size = wintypes.DWORD(256)
    username = ctypes.create_unicode_buffer(256)

    if ctypes.windll.advapi32.GetUserNameW(username, ctypes.byref(buffer_size)):
        return username.value
    else:
        return None

def get_registered_user():
    """ Read the registered user from file """
    if not os.path.exists(USER_FILE):
        return None

    with open(USER_FILE, "r") as file:
        return file.readline().strip().replace("Registered User: ", "")

def log_auth_attempt(success):
    """ Log authentication attempts with timestamp """
    user = get_current_user() or "Unknown User"
    status = "SUCCESS" if success else "FAILED"
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {user} - Authentication {status}\n")

def authenticate_user():
    """ Authenticate using Windows Hello """
    registered_user = get_registered_user()
    current_user = get_current_user()

    if not registered_user:
        print("Error: No user registered.")
        return False

    if current_user != registered_user:
        print(f"❌ User {current_user} is not registered. Access Denied.")
        log_auth_attempt(False)
        return False

    # Create authentication dialog
    app = QApplication(sys.argv)
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Windows Hello Authentication")
    msg_box.setText(f"Please authenticate, {current_user}.\nUse Fingerprint, Face ID, or PIN.")
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    result = msg_box.exec()

    if result == QMessageBox.StandardButton.Ok:
        print(f"✅ Authentication Successful for {current_user}")
        log_auth_attempt(True)
        return True
    else:
        print(f"❌ Authentication Failed for {current_user}")
        log_auth_attempt(False)
        return False

if __name__ == "__main__":
    authenticate_user()
