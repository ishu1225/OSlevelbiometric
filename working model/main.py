import store_reference
import authenticate

def main():
    print("Facial Recognition Authentication System")
    while True:
        choice = input("1. Store Reference Image\n2. Authenticate\n3. Exit\nChoose an option: ").strip()
        print(f"Selected option: {choice}")
        
        if choice == "1":
            source = input("Enter 'upload' or 'webcam': ").strip()
            print(f"Source selected: {source}")
            if source == "upload":
                camera_choice = input("Use camera instead of file upload? (yes/no): ").strip().lower()
                if camera_choice == "yes":
                    store_reference.store_reference_image(source="upload", use_camera=True)
                else:
                    file_path = input("Enter the image file path: ").strip()
                    print(f"File path provided: {file_path}")
                    store_reference.store_reference_image(source="upload", file_path=file_path)
            elif source == "webcam":
                store_reference.store_reference_image(source="webcam")
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