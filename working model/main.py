import store_reference
import authenticate
import os

def main():
    print("Facial Recognition Authentication System (Max 3 Users)")
    max_users = 3
    allowed_users = ["user1", "user2", "user3"]

    while True:
        choice = input("1. Store Reference Image\n2. Authenticate\n3. Exit\nChoose an option: ").strip()
        print(f"Selected option: {choice}")
        
        if choice == "1":
            current_users = [f for f in os.listdir("reference_images") if f.startswith("reference_") and f.endswith(".jpg")] if os.path.exists("reference_images") else []
            if len(current_users) >= max_users:
                print(f"Maximum of {max_users} users reached. You can overwrite an existing user.")
                overwrite = input("Would you like to overwrite an existing user? (yes/no): ").strip().lower()
                if overwrite != "yes":
                    continue
                user_id = input("Enter user to overwrite (user1, user2, user3): ").strip()
                if user_id not in allowed_users:
                    print("Invalid user ID. Use 'user1', 'user2', or 'user3'.")
                    continue
            else:
                user_id = input("Enter user ID (user1, user2, user3): ").strip()
                if user_id not in allowed_users:
                    print("Invalid user ID. Use 'user1', 'user2', or 'user3'.")
                    continue
                if os.path.exists(f"reference_images/reference_{user_id}.jpg"):
                    overwrite = input(f"{user_id} already exists. Overwrite? (yes/no): ").strip().lower()
                    if overwrite != "yes":
                        continue

            password = input("Enter registration password: ").strip()
            source = input("Enter 'upload' or 'webcam': ").strip()
            print(f"Source selected: {source}")
            if source == "upload":
                camera_choice = input("Use camera instead of file upload? (yes/no): ").strip().lower()
                if camera_choice == "yes":
                    store_reference.store_reference_image(user_id, password, source="upload", use_camera=True)
                else:
                    file_path = input("Enter the image file path: ").strip()
                    print(f"File path provided: {file_path}")
                    store_reference.store_reference_image(user_id, password, source="upload", file_path=file_path)
            elif source == "webcam":
                store_reference.store_reference_image(user_id, password, source="webcam")
            else:
                print("Invalid source.")
        elif choice == "2":
            source = input("Enter 'upload' or 'webcam': ").strip()
            print(f"Source selected: {source}")
            if source == "upload":
                camera_choice = input("Use camera instead of file upload? (yes/no): ").strip().lower()
                if camera_choice == "yes":
                    authenticate.authenticate_image(source="upload", use_camera=True)
                else:
                    file_path = input("Enter the image file path: ").strip()
                    print(f"File path provided: {file_path}")
                    authenticate.authenticate_image(source="upload", file_path=file_path)
            elif source == "webcam":
                authenticate.authenticate_image(source="webcam")
            else:
                print("Invalid source.")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()