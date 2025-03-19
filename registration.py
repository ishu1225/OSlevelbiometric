import sys
import os
import ctypes
from ctypes import wintypes
from PyQt6.QtWidgets import QApplication, QMessageBox

USER_FILE = "registered_user.txt"  # File to store registered user

def get_current_user():
    """ Get the current Windows username """
    buffer_size = wintypes.DWORD(256)
    username = ctypes.create_unicode_buffer(256)

    if ctypes.windll.advapi32.GetUserNameW(username, ctypes.byref(buffer_size)):
        return username.value
    else:
        return None

def register_user():
    """ Register the current Windows user for biometric authentication """
    user = get_current_user()
    if not user:
        print("Error: Unable to retrieve username.")
        return False

    # Save the registered user
    with open(USER_FILE, "w") as file:
        file.write(f"Registered User: {user}")

    print(f"✅ User {user} registered successfully.")
    return True

if __name__ == "__main__":
    register_user()
