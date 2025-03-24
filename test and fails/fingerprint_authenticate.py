import sys
import os
import ctypes
from ctypes import wintypes
from PyQt6.QtWidgets import QApplication, QMessageBox

AUTH_FILE = "auth_status.txt"  # File to store authenticated user

def get_current_user():
    """ Get the current Windows username correctly """
    buffer_size = wintypes.DWORD(256)
    username = ctypes.create_unicode_buffer(256)

    if ctypes.windll.advapi32.GetUserNameW(username, ctypes.byref(buffer_size)):
        return username.value
    else:
        return None

def is_authenticated():
    """ Check if the current user is already authenticated """
    if not os.path.exists(AUTH_FILE):
        return False

    with open(AUTH_FILE, "r") as file:
        saved_user = file.readline().strip().replace("Authenticated User: ", "")

    return saved_user == get_current_user()

def windows_hello_auth():
    """ Trigger Windows Hello authentication and verify user """
    user = get_current_user()
    if not user:
        print("Error: Unable to retrieve username.")
        return False

    if is_authenticated():
        print(f"✅ User {user} is already authenticated. No need to re-authenticate.")
        return True

    # Create a Windows authentication dialog
    app = QApplication(sys.argv)
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Windows Hello Authentication")
    msg_box.setText(f"Please authenticate, {user}.\nUse Fingerprint, Face ID, or PIN.")
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()

    # Save authentication status
    with open(AUTH_FILE, "w") as file:
        file.write(f"Authenticated User: {user}")

    print(f"✅ Authentication Successful for {user}")
    return True

# Run authentication check
if windows_hello_auth():
    print("✅ Authentication Matched or Successfully Completed.")
else:
    print("❌ Authentication Failed.")
