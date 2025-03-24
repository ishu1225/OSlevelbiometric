import cv2
import face_recognition
import os

def authenticate_image(source="upload", file_path=None, use_camera=False):
    # Check if reference image exists
    ref_path = "reference_images/reference.jpg"
    if not os.path.exists(ref_path):
        print("No reference image found. Please store a reference image first.")
        return False

    # Load the reference image
    print("Loading reference image...")
    reference_image = face_recognition.load_image_file(ref_path)
    reference_encodings = face_recognition.face_encodings(reference_image)
    if not reference_encodings:
        print("No faces detected in the reference image. Please store a valid image with a face.")
        return False
    reference_encoding = reference_encodings[0]

    # Load or capture the new image
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

    # Detect faces in the new image
    print("Detecting faces in the new image...")
    face_locations = face_recognition.face_locations(new_image)
    if len(face_locations) == 0:
        print("No face detected in the new image.")
        return False
    elif len(face_locations) > 1:
        print("Multiple faces detected. Please provide an image with only one face.")
        return False

    # Get face encoding for the new image
    new_encoding = face_recognition.face_encodings(new_image)[0]

    # Compare the faces
    results = face_recognition.compare_faces([reference_encoding], new_encoding)
    if results[0]:
        print("Authentication successful! Faces match.")
        return True
    else:
        print("Authentication failed! Faces do not match.")
        return False

# Example usage
if __name__ == "__main__":
    authenticate_image(source="upload", file_path="path_to_new_image.jpg")