import tkinter as tk
from PIL import Image, ImageTk
from datetime import date
import time
import numpy as np
import cv2
from tkinter.filedialog import askopenfilename
import os
import shutil
import Train_FDD_cnn as TrainM
import smtplib
from email.message import EmailMessage
import imghdr
import winsound

# ================= GUI SETUP =================
root = tk.Tk()
root.configure(background="brown")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
root.title("Exam Suspicious Activity Detection")

# ================= BACKGROUND =================
image2 = Image.open('6.webp')
image2 = image2.resize((w, h), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0)

# ================= TITLE =================
label_l1 = tk.Label(root,
    text="Exam Hall Suspicious Activity Detection",
    font=("Times New Roman", 30, 'bold'),
    background="#B0E0E6", fg="black",
    width=70, height=2)
label_l1.place(x=0, y=0)

# ================= FUNCTIONS =================
def CLOSE():
    root.destroy()

def update_label(text):
    lbl = tk.Label(root, text=text, width=50,
                   font=("bold", 20),
                   bg='cyan', fg='black')
    lbl.place(x=400, y=500)

def train_model():
    update_label("Training started...")
    start = time.time()

    X = TrainM.main()

    end = time.time()
    msg = f"Training Completed\n{X}\nTime: {end-start:.2f}s"
    update_label(msg)

# ================= VIDEO DISPLAY =================
def run_video(path, x, y, w, h):
    cap = cv2.VideoCapture(path)

    def show_frame():
        ret, frame = cap.read()
        if not ret:
            return

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image).resize((w, h))
        imgtk = ImageTk.PhotoImage(image=img)

        label = tk.Label(root)
        label.place(x=x, y=y)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        label.after(10, show_frame)

    show_frame()

# ================= FILE SELECT =================
def VIDEO():
    fileName = askopenfilename(filetypes=[("Video files", "*.mp4 *.mov")])
    if fileName:
        run_video(fileName, 560, 190, 753, 485)

# ================= EMAIL =================
def mail():
    Sender_Email = "sakshir132004@gmail.com"
    Reciever_Email = "latesukanya2@gmail.com"
    Password = 'whvr ijjz beyg ijpm'

    msg = EmailMessage()
    msg['Subject'] = "Suspicious Activity Alert"
    msg['From'] = Sender_Email
    msg['To'] = Reciever_Email

    with open('abc.png', 'rb') as f:
        img_data = f.read()
        img_type = imghdr.what(f.name)

    msg.add_attachment(img_data, maintype='image',
                       subtype=img_type, filename='alert.png')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('sakshir132004@gmail.com', 'whvr ijjz beyg ijpm') 
        smtp.send_message(msg)

# ================= BUZZER =================
def activate_buzzer():
    try:
        winsound.Beep(1000, 1000)
    except:
        print("Buzzer not supported")

# ================= DETECTION =================
def show_FDD_video(video_path):
    from keras.models import load_model

    model = load_model('model.h5', compile=False)
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img = cv2.resize(frame, (64, 64))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.reshape(-1, 64, 64, 1) / 255.0

        pred = model.predict(img)

        if pred[0][0] < 0.5:
            label = "Suspicious Activity!"
            color = (0, 0, 255)

            cv2.imwrite('abc.png', frame)
            mail()
            activate_buzzer()
        else:
            label = "Normal"
            color = (0, 255, 0)

        cv2.putText(frame, label, (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("Detection", frame)

        if cv2.waitKey(30) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def Video_Verify():
    fileName = askopenfilename(filetypes=[("Video files", "*.mp4 *.mov")])
    if fileName:
        show_FDD_video(fileName)

# ================= FACE AUTH (FIXED) =================
def face_auth():
        from subprocess import call
        call(["python","Face_Authantication.py"])
        root.destroy()

# ================= BUTTONS =================
btn1 = tk.Button(root, text="Open Video",
                 command=Video_Verify,
                 width=15, height=1,
                 font=('times', 20, 'bold'),
                 bg="#B0E0E6")
btn1.place(x=400, y=250)

btn2 = tk.Button(root, text="Exit",
                 command=CLOSE,
                 width=15, height=1,
                 font=('times', 20, 'bold'),
                 bg="#B0E0E6")
btn2.place(x=400, y=330)

btn3 = tk.Button(root, text="Face Authentication",
                 command=face_auth,   # ✅ FIXED
                 width=20, height=1,
                 font=('times', 20, 'bold'),
                 bg="#B0E0E6")
btn3.place(x=400, y=430)

# ================= MAIN =================
root.mainloop()