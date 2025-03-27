import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import cv2
import face_recognition
import store_reference
import authenticate
import os
import threading
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np

# Global camera object for pre-initialization
global_camera = None

# Create a gradient background image using Pillow
def create_gradient(width, height, color1, color2):
    image = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(image)
    r1, g1, b1 = [int(color1[i:i+2], 16) for i in (1, 3, 5)]
    r2, g2, b2 = [int(color2[i:i+2], 16) for i in (1, 3, 5)]
    
    for y in range(height):
        r = int(r1 + (r2 - r1) * y / height)
        g = int(g1 + (g2 - g1) * y / height)
        b = int(b1 + (b2 - b1) * y / height)
        draw.line((0, y, width, y), fill=(r, g, b))
    
    return ImageTk.PhotoImage(image)

# Custom button hover effect with scale animation
def on_enter(e, btn, original_bg, hover_bg):
    btn['background'] = hover_bg
    btn.configure(cursor="hand2")
    # Scale up slightly
    btn.place(relx=float(btn.place_info()['relx']), 
              rely=float(btn.place_info()['rely']), 
              relwidth=float(btn.place_info()['relwidth']) * 1.05, 
              relheight=float(btn.place_info()['relheight']) * 1.05)

def on_leave(e, btn, original_bg, hover_bg):
    btn['background'] = original_bg
    btn.configure(cursor="")
    # Scale back to original size
    btn.place(relx=float(btn.place_info()['relx']), 
              rely=float(btn.place_info()['rely']), 
              relwidth=float(btn.place_info()['relwidth']) / 1.05, 
              relheight=float(btn.place_info()['relheight']) / 1.05)

# Initialize the camera at startup to reduce delay
def initialize_camera():
    global global_camera
    print("Initializing camera at startup...")
    global_camera = cv2.VideoCapture(0)
    
    if not global_camera.isOpened():
        print("Error: Failed to initialize webcam. Trying alternative backend...")
        global_camera = cv2.VideoCapture(0, cv2.CAP_ANY)
        if not global_camera.isOpened():
            messagebox.showerror("Error", "Failed to initialize webcam. Please check your camera.")
            return False
    
    global_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    global_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    width = global_camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = global_camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Camera initialized with resolution: {width}x{height}")
    return True

# Function to capture webcam image using the pre-initialized camera
def capture_webcam_image(show_success_message=True):
    global global_camera
    if global_camera is None or not global_camera.isOpened():
        messagebox.showerror("Error", "Webcam not initialized.")
        return None
    
    captured_image = None
    
    def process_feed():
        nonlocal captured_image
        while True:
            ret, frame = global_camera.read()
            if not ret:
                print("Error: Failed to capture frame.")
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
                print(f"Image captured and saved as {captured_image}")
                break
            
            if key == ord('q') or key == ord('Q'):
                print("User quit the webcam feed.")
                break
        
        cv2.destroyAllWindows()
        return
    
    thread = threading.Thread(target=process_feed)
    thread.start()
    thread.join()
    
    if captured_image and show_success_message:
        messagebox.showinfo("Success", "Image Captured Successfully!")
    elif not captured_image:
        print("No image captured.")
    
    return captured_image

# Store Reference Image UI
def show_store_ui():
    store_window = tk.Toplevel(root)
    store_window.title("Store Reference Image")
    store_window.geometry("700x630")
    store_window.resizable(False, False)

    gradient = create_gradient(700, 630, "#7B5BFF", "#A78BFA")
    bg_label = tk.Label(store_window, image=gradient)
    bg_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(store_window, bg="#5E35B1", bd=0, highlightthickness=0)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

    tk.Label(
        frame, 
        text="Register New User", 
        fg="#FFFFFF", 
        bg="#5E35B1", 
        font=("Arial", 28, "bold")
    ).pack(pady=30)

    input_frame = tk.Frame(frame, bg="#5E35B1")
    input_frame.pack(pady=15)

    tk.Label(
        input_frame, 
        text="User ID (user1, user2, user3):", 
        fg="#EDE7F6", 
        bg="#5E35B1", 
        font=("Arial", 18)
    ).grid(row=0, column=0, padx=15, pady=8, sticky="w")
    user_id_entry = ttk.Entry(
        input_frame, 
        font=("Arial", 18), 
        width=20
    )
    user_id_entry.grid(row=1, column=0, padx=15, pady=8)

    tk.Label(
        input_frame, 
        text="Password:", 
        fg="#EDE7F6", 
        bg="#5E35B1", 
        font=("Arial", 18)
    ).grid(row=2, column=0, padx=15, pady=8, sticky="w")
    password_entry = ttk.Entry(
        input_frame, 
        show="*", 
        font=("Arial", 18), 
        width=20
    )
    password_entry.grid(row=3, column=0, padx=15, pady=8)

    def store_image():
        user_id = user_id_entry.get().strip().lower()
        password = password_entry.get()
        
        if not user_id or not password:
            messagebox.showerror("Error", "Please enter User ID and Password")
            return
        
        # Check if the password matches the required password
        REQUIRED_PASSWORD = "240204"
        if password != REQUIRED_PASSWORD:
            messagebox.showerror("Error", "Incorrect password. Please enter the correct password to register.")
            return
        
        choice = messagebox.askquestion("Choose Input Method", "Do you want to capture from webcam? (Select 'No' to upload an image)")
        if choice == 'yes':
            file_path = capture_webcam_image(show_success_message=True)
        else:
            file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        
        if not file_path:
            return
        
        loading_label = tk.Label(
            frame, 
            text="Processing...", 
            fg="#EDE7F6", 
            bg="#5E35B1", 
            font=("Arial", 16, "italic")
        )
        loading_label.pack(pady=8)
        store_window.update()

        success = store_reference.store_reference_image(user_id, password, source="upload", file_path=file_path)
        loading_label.destroy()
        
        if success:
            messagebox.showinfo("Success", "Reference image stored successfully!")
            store_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to store reference image")

    # Bind the Enter key to trigger the store_image function
    store_window.bind('<Return>', lambda event: store_image())

    register_icon = ImageTk.PhotoImage(Image.open("register_icon.png").resize((30, 30)) if os.path.exists("register_icon.png") else Image.new("RGBA", (30, 30), (0, 0, 0, 0)))
    register_btn = tk.Button(
        frame, 
        text=" Register User", 
        image=register_icon, 
        compound="left", 
        command=store_image, 
        font=("Arial", 18, "bold"), 
        bg="#7B5BFF", 
        fg="#FFFFFF", 
        activebackground="#5E35B1", 
        activeforeground="#FFFFFF", 
        relief="flat", 
        padx=30, 
        pady=12,
        borderwidth=0,
        highlightthickness=0
    )
    register_btn.image = register_icon
    register_btn.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.5, relheight=0.1)
    register_btn.bind("<Enter>", lambda e: on_enter(e, register_btn, "#7B5BFF", "#9575CD"))
    register_btn.bind("<Leave>", lambda e: on_leave(e, register_btn, "#7B5BFF", "#9575CD"))

# Create Main Window
root = tk.Tk()
root.title("Face Recognition System")
root.geometry("1000x800")
root.resizable(False, False)

# Initialize the camera at startup
if not initialize_camera():
    root.quit()

gradient = create_gradient(1000, 800, "#7B5BFF", "#A78BFA")
bg_label = tk.Label(root, image=gradient)
bg_label.place(relwidth=1, relheight=1)

main_frame = tk.Frame(root, bg="#9575CD", bd=0, highlightthickness=0)
main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

tk.Label(
    main_frame, 
    text="Face Recognition System", 
    fg="#FFFFFF", 
    bg="#9575CD", 
    font=("Arial", 40, "bold")
).pack(pady=40)

tk.Label(
    main_frame, 
    text="Secure Authentication with Facial Recognition", 
    fg="#EDE7F6", 
    bg="#9575CD", 
    font=("Arial", 24, "italic")
).pack(pady=10)

store_icon = ImageTk.PhotoImage(Image.open("store_icon.png").resize((40, 40)) if os.path.exists("store_icon.png") else Image.new("RGBA", (40, 40), (0, 0, 0, 0)))
store_option_btn = tk.Button(
    main_frame, 
    text=" Store Reference Image", 
    image=store_icon, 
    compound="left", 
    command=show_store_ui, 
    font=("Arial", 24, "bold"), 
    bg="#5E35B1", 
    fg="#FFFFFF", 
    activebackground="#4527A0", 
    activeforeground="#FFFFFF", 
    relief="flat", 
    padx=40, 
    pady=20,
    borderwidth=0,
    highlightthickness=0
)
store_option_btn.image = store_icon
store_option_btn.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.6, relheight=0.1)
store_option_btn.bind("<Enter>", lambda e: on_enter(e, store_option_btn, "#5E35B1", "#7E57C2"))
store_option_btn.bind("<Leave>", lambda e: on_leave(e, store_option_btn, "#5E35B1", "#7E57C2"))

# Authenticate directly without an intermediate window
def authenticate_user():
    file_path = capture_webcam_image(show_success_message=False)
    if not file_path:
        return
    
    loading_label = tk.Label(
        main_frame, 
        text="Authenticating...", 
        fg="#EDE7F6", 
        bg="#9575CD", 
        font=("Arial", 20, "italic")
    )
    loading_label.pack(pady=10)
    root.update()

    user_id = authenticate.authenticate_image(source="upload", file_path=file_path)
    loading_label.destroy()
    
    if user_id:
        messagebox.showinfo("Success", f"Welcome {user_id.capitalize()}! Authentication Successful!")
    else:
        messagebox.showerror("Error", "Authentication Failed")

auth_icon = ImageTk.PhotoImage(Image.open("auth_icon.png").resize((40, 40)) if os.path.exists("auth_icon.png") else Image.new("RGBA", (40, 40), (0, 0, 0, 0)))
auth_option_btn = tk.Button(
    main_frame, 
    text=" Authenticate", 
    image=auth_icon, 
    compound="left", 
    command=authenticate_user, 
    font=("Arial", 24, "bold"), 
    bg="#7B5BFF", 
    fg="#FFFFFF", 
    activebackground="#5E35B1", 
    activeforeground="#FFFFFF", 
    relief="flat", 
    padx=40, 
    pady=20,
    borderwidth=0,
    highlightthickness=0
)
auth_option_btn.image = auth_icon
auth_option_btn.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.6, relheight=0.1)
auth_option_btn.bind("<Enter>", lambda e: on_enter(e, auth_option_btn, "#7B5BFF", "#9575CD"))
auth_option_btn.bind("<Leave>", lambda e: on_leave(e, auth_option_btn, "#7B5BFF", "#9575CD"))

exit_icon = ImageTk.PhotoImage(Image.open("exit_icon.png").resize((40, 40)) if os.path.exists("exit_icon.png") else Image.new("RGBA", (40, 40), (0, 0, 0, 0)))
exit_btn = tk.Button(
    main_frame, 
    text=" Exit", 
    image=exit_icon, 
    compound="left", 
    command=root.quit, 
    font=("Arial", 24, "bold"), 
    bg="#D81B60", 
    fg="#FFFFFF", 
    activebackground="#AD1457", 
    activeforeground="#FFFFFF", 
    relief="flat", 
    padx=40, 
    pady=20,
    borderwidth=0,
    highlightthickness=0
)
exit_btn.image = exit_icon
exit_btn.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.6, relheight=0.1)
exit_btn.bind("<Enter>", lambda e: on_enter(e, exit_btn, "#D81B60", "#EC407A"))
exit_btn.bind("<Leave>", lambda e: on_leave(e, exit_btn, "#D81B60", "#EC407A"))

# Ensure the camera is released when the application closes
def on_closing():
    global global_camera
    if global_camera is not None:
        global_camera.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()