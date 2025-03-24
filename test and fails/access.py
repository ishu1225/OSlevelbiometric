import os
from authentication import authenticate_user

SECURE_FILE = "protected_data.txt"

def access_secure_file():
    """ Restrict file access to authenticated users """
    if authenticate_user():
        print("Access granted to secure file!")
        
        if os.path.exists(SECURE_FILE):
            with open(SECURE_FILE, "r") as file:
                print(" Secure File Contents:\n")
                print(file.read())
        else:
            print("Secure file does not exist. Creating one.")
            with open(SECURE_FILE, "w") as file:
                file.write("This is sensitive data. Do not share!")

    else:
        print("Access Denied!")

if __name__ == "__main__":
    access_secure_file()
