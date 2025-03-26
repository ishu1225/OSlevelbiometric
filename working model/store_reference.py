import cv2
import face_recognition
import os

def store_reference_image(user_id, password, source="upload", file_path=None, use_camera=False):
    # Fixed password check
    correct_password = "240204"
    if password != correct_password:
        print("Incorrect password. Registration failed.")
        return False

    print(f"Starting reference image storage for {user_id} with source: {source}")
    
    if not os.path.exists("reference_images"):
        os.makedirs("reference_images")

    ref_path = f"reference_images/reference_{user_id}.jpg"

    if source == "upload":
        if use_camera:
            print("Capturing image from webcam...")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                image = frame
            else:
                print("Error: Could not capture image from webcam.")
                cap.release()
                return False
            cap.release()
            cv2.destroyAllWindows()
        elif file_path:
            if not os.path.isfile(file_path):
                print(f"Error: File '{file_path}' does not exist.")
                return False
            print(f"Loading image from: {file_path}")
            try:
                image = face_recognition.load_image_file(file_path)
            except Exception as e:
                print(f"Error loading image: {e}")
                return False
        else:
            print("No file path provided and camera not selected.")
            return False
    elif source == "webcam":
        print("Capturing image from webcam...")
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            image = frame
        else:
            print("Error: Could not capture image from webcam.")
            cap.release()
            return False
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Invalid source.")
        return False

    print("Detecting faces in the image...")
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) == 0:
        print("No face detected in the image.")
        return False
    elif len(face_locations) > 1:
        print("Multiple faces detected. Please upload an image with only one face.")
        return False

    cv2.imwrite(ref_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    print(f"Reference image for {user_id} stored successfully!")
    return True

if __name__ == "__main__":
    store_reference_image("user1", "240204", source="upload", file_path="path_to_your_image.jpg")