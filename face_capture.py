import cv2
import os

# Create directory if it doesn't exist
if not os.path.exists("biometric_data"):
    os.makedirs("biometric_data")

# Start camera
cam = cv2.VideoCapture(2)
cv2.namedWindow("Capture Face")

while True:
    import time
    time.sleep(2)  # Wait 2 seconds before capturing
    ret, frame = cam.read()

    if not ret:
        print("❌ Failed to grab frame")
        break
    cv2.imshow("Capture Face", frame)

    # Press 's' to save the image
    if cv2.waitKey(1) & 0xFF == ord('s'):
       img_name = os.path.join("biometric_data", "user_face.jpg")
       cv2.imwrite(img_name, frame)
       print(f"✅ Image saved: {img_name}")
       break

cam.release()
cv2.destroyAllWindows()
