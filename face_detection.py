import cv2
import numpy as np
from tkinter import ttk
from tkinter import Tk  # Nhập khẩu Tk từ tkinter
import tkinter as tk  # Nhập khẩu tk
from PIL import Image, ImageTk 
import threading

def face_real_time(scale_factor, min_neighbor):
    global video_capture
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Khong mo duoc webcam!!")
        return
    
    while not stop_event.is_set():  # Kiểm tra sự kiện dừng
        ret,frame = video_capture.read()
        if not ret:
            break
        #Lật ngược lại cam 
        frame = cv2.flip(frame,1)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = scale_factor, minNeighbors = min_neighbor)
        
        #(Anonymize faces)
        for (x, y, w, h) in faces:
            method = anonymize_method.get()
            if method == "Blur": 
                blur_amount = blur_level.get()# Lấy giá trị từ Trackbar
                blur_face(frame, x, y, w, h, blur_amount)
            elif method == "Pixelate":
                pixelization(frame, x, y, w, h, pixel_size=10)
            elif method == "Emoji":
                replace_with_emoji(frame, x, y, w, h)

        root.after(0, update_image, frame)        
  
    video_capture.release()
    cv2.destroyAllWindows()    


def blur_face(img, x, y, w, h, blur_amount):
    # Đảm bảo blur_amount là số lẻ và lớn hơn 1
    blur_amount = max(1, min(99, blur_amount // 2 * 2 + 1))
    face = img[y:y+h, x:x+w]
    blur_face = cv2.GaussianBlur(face, (blur_amount, blur_amount), 30)
    img[y:y+h, x:x+w] = blur_face

def pixelization(img, x, y, w, h, pixel_size):
    face = img[y: y+h, x: x+w]
    face = cv2.resize(face, (pixel_size, pixel_size), interpolation = cv2.INTER_LINEAR)
    face = cv2.resize(face, (w, h), interpolation =  cv2.INTER_NEAREST)
    img[y: y+h, x: x+w] = face

def replace_with_emoji(img, x, y, w, h):
    emoji = cv2.imread('emoji.jpg')
    emoji = cv2.resize(emoji, (w,h))
    img[y: y+h, x: x+w] = emoji

def update_anonymize_method(method):
    anonymize_method.set(method)   

def on_closing():
    stop_event.set()  # Đặt sự kiện dừng
    root.quit()  # Dừng vòng lặp Tkinter   

def update_image(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Chuyển đổi từ BGR sang RGB
    imgtk = ImageTk.PhotoImage(image=img)  # Tạo đối tượng PhotoImage từ ảnh
    video_label.imgtk = imgtk  # Giữ tham chiếu đến ảnh để tránh garbage collection
    video_label.configure(image=imgtk)  # Cập nhật label với ảnh mới      

stop_event = threading.Event()

root = Tk()
root.title("Face Anonymization Application")
anonymize_method = tk.StringVar(value="Blur")
blur_level = tk.IntVar(value=1)

method_frame = ttk.Frame(root)
method_frame.pack(pady=20)


pixelate_button = ttk.Button(method_frame, text="Pixelate", command=lambda: update_anonymize_method("Pixelate"))
pixelate_button.grid(row=0, column=1, padx=10)

emoji_button = ttk.Button(method_frame, text="Emoji", command=lambda: update_anonymize_method("Emoji"))
emoji_button.grid(row=0, column=2, padx=10)


blur_button = ttk.Button(method_frame, text="Blur", command=lambda: update_anonymize_method("Blur"))
blur_button.grid(row=0, column=0, padx=10)

blur_scale = ttk.Scale(method_frame, from_=1, to=99, variable=blur_level, orient=tk.HORIZONTAL)
blur_scale.grid(row=1, column=0, padx=10)
blur_scale.set(1)  # Đặt giá trị mặc định cho Trackbar


video_label = ttk.Label(root)
video_label.pack(pady=40)

video_thread = threading.Thread(target=face_real_time, args=(1.1, 6))
video_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Chạy giao diện người dùng
root.mainloop()

# Đặt sự kiện dừng trước khi chờ luồng video kết thúc
stop_event.set()
video_thread.join()

