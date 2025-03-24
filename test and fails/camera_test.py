import cv2

cam = cv2.VideoCapture(0)
backend = cam.getBackendName() if hasattr(cam, 'getBackendName') else "Unknown"

print(f"✅ Camera is working with backend: {backend}")

cam.release()
