import cv2
import face_recognition
import os

def authenticate_image(source="upload", file_path=None, use_camera=False):
    if not os.path.exists("reference_images"):
        print("No reference images found. Please store a reference image first.")
        return False

    reference_encodings = {}
    for user_id in ["user1", "user2", "user3"]:
        ref_path = f"reference_images/reference_{user_id}.jpg"
        if os.path.exists(ref_path):
            print(f"Loading reference image for {user_id}...")
            reference_image = face_recognition.load_image_file(ref_path)
            encodings = face_recognition.face_encodings(reference_image)
            if encodings:
                reference_encodings[user_id] = encodings[0]
            else:
                print(f"No faces detected in reference image for {user_id}.")

    if not reference_encodings:
        print("No valid reference images with detectable faces found.")
        return False

    if source == "upload":
        if use_camera:
            print("Capturing image from webcam...")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                new_image = frame
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
            print(f"Loading new image from: {file_path}")
            new_image = face_recognition.load_image_file(file_path)
        else:
            print("No file path provided and camera not selected.")
            return False
    elif source == "webcam":
        print("Capturing image from webcam...")
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            new_image = frame
        else:
            print("Error: Could not capture image from webcam.")
            cap.release()
            return False
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Invalid source.")
        return False

    print("Detecting faces in the new image...")
    face_locations = face_recognition.face_locations(new_image)
    if len(face_locations) == 0:
        print("No face detected in the new image.")
        return False
    elif len(face_locations) > 1:
        print("Multiple faces detected. Please provide an image with only one face.")
        return False

    new_encoding = face_recognition.face_encodings(new_image)[0]

    for user_id, ref_encoding in reference_encodings.items():
        results = face_recognition.compare_faces([ref_encoding], new_encoding)
        if results[0]:
             print(f"Authentication successful! Matched with {user_id}.")
             return user_id  # Return the actual user ID

    print("Authentication failed! No match found with any user.")
    return False

if __name__ == "__main__":
    authenticate_image(source="upload", file_path="path_to_new_image.jpg")
