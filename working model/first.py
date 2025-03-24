import cv2
import dlib
import face_recognition
import numpy as np

# Load an image (replace 'test.jpg' with your image path)
image_path = "test.jpg"  # Make sure you have an image in the same directory
image = cv2.imread(image_path)

# Convert image from BGR (OpenCV format) to RGB (face_recognition format)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect faces using face_recognition
face_locations = face_recognition.face_locations(rgb_image)

# Draw rectangles around detected faces
for top, right, bottom, left in face_locations:
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

# Display the image
cv2.imshow("Face Detection Test", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
