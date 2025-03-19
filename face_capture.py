import cv2

print("Trying to open the camera...")

# Try MSMF backend first
cam = cv2.VideoCapture(0, cv2.CAP_MSMF)

if not cam.isOpened():
    print("MSMF failed. Trying DSHOW...")
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cam.isOpened():
    print("DSHOW failed. Trying default backend...")
    cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Camera is not accessible. Check settings.")
    exit()

print("Camera opened successfully.")

# Set frame width and height
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("Frame not captured.")
        break

    # Ensure correct format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cv2.imshow("Face Capture", frame)

    key = cv2.waitKey(1)
    if key == ord('s'):  # Save image
        cv2.imwrite("face.jpg", frame)
        print("Image saved as face.jpg")
        break
    elif key == ord('q'):  # Exit without saving
        print("Exiting without saving.")
        break

cam.release()
cv2.destroyAllWindows()
print("Camera released successfully.")
