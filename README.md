Face Recognition System
Overview
This project implements a secure facial recognition system with a graphical user interface (GUI) built using Python and Tkinter. The system allows users to:
- Register themselves by storing facial reference images
- Authenticate themselves using facial recognition
- Manage a limited number of users with password protection

The system uses the `face_recognition` library, which is built on top of dlib's state-of-the-art face recognition capabilities, along with OpenCV for camera operations and image processing.

Features
1. **User Registration**
- Password-protected registration (password: "240204")
- Supports both webcam capture and image upload
- Limits to 3 predefined users (user1, user2, user3)
- Prevents duplicate registrations unless explicitly overwritten
- Real-time face detection during webcam capture

2. **Authentication**
- Real-time face detection and matching
- Handles single-face authentication only (rejects multiple faces)
- Provides clear feedback on authentication results
- Visual face detection during capture

3. **Security Features**
- Password protection for registration
- Face validation during registration (ensures exactly one face)
- Secure storage of reference images in a dedicated directory

4. **User Interface**
- Modern gradient-based UI with hover effects
- Responsive buttons with icons
- Clear error and success messages
- Webcam feed visualization during capture

Installation
**Prerequisites:**
- Python 3.6 or higher
- pip package manager

**Install dependencies:**
```
pip install face-recognition opencv-python pillow numpy
```

**Run the application:**
```
python face_recognition_ui.py
```

Usage Guide
1. **Registration Process**
- Click "Store Reference Image" on the main screen
- Enter one of the allowed user IDs (`user1`, `user2`, or `user3`)
- Enter the system password (`240204`)
- Choose between:
  - **Webcam capture** (press 'C' to capture, 'Q' to quit)
  - **Image upload** (select a file from your system)
- The system will validate the image contains exactly one face
- On success, the reference image will be stored in the `reference_images` directory

2. **Authentication Process**
- Click "Authenticate" on the main screen
- The webcam will open - position your face clearly
- Press 'C' to capture your image
- The system will:
  - Detect faces in the captured image
  - Compare with stored reference images
  - Return a match or error message

Limitations
- Limited to 3 predefined users
- No database integration for user management
- No encryption for stored reference images
- Password is hardcoded (not suitable for production)

Future Enhancements
- Implement proper password hashing
- Add encryption for stored images
- Implement session management
- Add user management interface
- Implement live video authentication
- Add GPU acceleration support

Conclusion
This face recognition system provides a solid foundation for facial authentication applications. With its clean interface and robust functionality, it demonstrates key concepts in biometric authentication while remaining accessible for further development.
