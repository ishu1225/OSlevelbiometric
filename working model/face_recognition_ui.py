import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
import face_recognition
import store_reference
import authenticate
import os
import threading

def capture_webcam_image():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Reduce frame width
    cap.set(4, 480)  # Reduce frame height
    captured_image = None
    
    def process_feed():
        nonlocal captured_image
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            cv2.imshow("Webcam - Press 'C' to Capture", frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('c') or key == ord('C'):
                captured_image = "captured_face.jpg"
                cv2.imwrite(captured_image, frame)
                break
            
            if key == ord('q') or key == ord('Q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return
    
    # Run webcam processing in a separate thread
    thread = threading.Thread(target=process_feed)
    thread.start()
    thread.join()
    
    if captured_image:
        messagebox.showinfo("Success", "Image Captured Successfully!")
    return captured_image

def show_store_ui():
    store_window = tk.Toplevel(root)
    store_window.title("Store Reference Image")
    store_window.geometry("400x350")
    store_window.configure(bg="#1e1e2e")
    
    tk.Label(store_window, text="User ID:", fg="white", bg="#1e1e2e", font=("Arial", 12, "bold")).pack(pady=5)
    user_id_entry = tk.Entry(store_window, font=("Arial", 12))
    user_id_entry.pack(pady=5)
    
    tk.Label(store_window, text="Password:", fg="white", bg="#1e1e2e", font=("Arial", 12, "bold")).pack(pady=5)
    password_entry = tk.Entry(store_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)
    
    def store_image():
        user_id = user_id_entry.get().strip().lower()
        password = password_entry.get()
        
        if not user_id or not password:
            messagebox.showerror("Error", "Please enter User ID and Password")
            return
        
        choice = messagebox.askquestion("Choose Input Method", "Do you want to capture from webcam? (Select 'No' to upload an image)")
        if choice == 'yes':
            file_path = capture_webcam_image()
        else:
            file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        
        if not file_path:
            return
        
        success = store_reference.store_reference_image(user_id, password, source="upload", file_path=file_path)
        if success:
            messagebox.showinfo("Success", "Reference image stored successfully!")
            store_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to store reference image")
    
    tk.Button(store_window, text="Register User", command=store_image, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=5)

def show_authenticate_ui():
    auth_window = tk.Toplevel(root)
    auth_window.title("Authenticate User")
    auth_window.geometry("400x250")
    auth_window.configure(bg="#1e1e2e")
    
    def authenticate_user():
        file_path = capture_webcam_image()
        if not file_path:
            return
        
        user_id = authenticate.authenticate_image(source="upload", file_path=file_path)
        
        if user_id:
            messagebox.showinfo("Success", f"Welcome {user_id.capitalize()}! Authentication Successful!")
            auth_window.destroy()
        else:
            messagebox.showerror("Error", "Authentication Failed")
    
    auth_btn = tk.Button(auth_window, text="Open Webcam & Authenticate", command=authenticate_user, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", padx=10, pady=5)
    auth_btn.pack(pady=10)

# Create main window
root = tk.Tk()
root.title("Face Recognition System")
root.geometry("400x250")
root.configure(bg="#1e1e2e")

tk.Label(root, text="Select an Option:", fg="white", bg="#1e1e2e", font=("Arial", 14, "bold")).pack(pady=10)

store_option_btn = tk.Button(root, text="Store Reference Image", command=show_store_ui, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
store_option_btn.pack(pady=5)

auth_option_btn = tk.Button(root, text="Authenticate", command=show_authenticate_ui, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", padx=10, pady=5)
auth_option_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12, "bold"), bg="#F44336", fg="white", padx=10, pady=5)
exit_btn.pack(pady=10)

root.mainloop()
