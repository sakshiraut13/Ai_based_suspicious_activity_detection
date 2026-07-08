from tkinter import *
import tkinter as tk
from tkinter import ttk, END, messagebox as ms
import numpy as np
import cv2
import os
from PIL import Image, ImageTk
import sqlite3
from subprocess import call

##############################################
root = tk.Tk()
root.configure(background="seashell2")
root.title("Face Authentication")

# Full screen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

# Database
my_conn = sqlite3.connect('face.db')

# Background
image2 = Image.open('4.jpg')
image2 = image2.resize((w, h), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
tk.Label(root, image=background_image).place(x=0, y=0)

# Title
tk.Label(root, text="Suspicious Activity Face Detection",
         font=('times', 40, 'bold'),
         bg="black", fg="yellow").place(x=330, y=5)

# Frame
frame_alpr = tk.LabelFrame(root, text=" --Process-- ",
                           width=280, height=400, bd=5,
                           font=('times', 15, 'bold'),
                           bg="seashell4")
frame_alpr.place(x=70, y=130)

##############################################

def Create_database():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    user_id = entry2.get()
    sampleN = 0

    if not os.path.exists("facesData"):
        os.makedirs("facesData")

    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleN += 1
            cv2.imwrite(f"facesData/User.{user_id}.{sampleN}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Capturing Face Data', img)

        if cv2.waitKey(1) == 27 or sampleN > 80:
            break

    cap.release()
    cv2.destroyAllWindows()
    entry2.delete(0, 'end')
    ms.showinfo("Success", "Face data created!")

##############################################

def Train_database():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except:
        ms.showerror("Error", "Install opencv-contrib-python")
        return

    path = "facesData"

    faces, IDs = [], []

    for file in os.listdir(path):
        parts = file.split(".")
        if len(parts) >= 3 and parts[1].isdigit():
            img = Image.open(os.path.join(path, file)).convert('L')
            faces.append(np.array(img, 'uint8'))
            IDs.append(int(parts[1]))

    if len(faces) == 0:
        ms.showerror("Error", "No face data found!")
        return

    recognizer.train(faces, np.array(IDs))
    recognizer.save("trainingData.yml")

    ms.showinfo("Success", "Training Completed!")

##############################################

def Test_database():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainingData.yml')
    except:
        ms.showerror("Error", "Train data missing or OpenCV issue")
        return

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            print(conf,"conf")

            if conf < 70:

                # ✅ AUTHORIZED
                text = "Authorized Person"
                color = (0, 255, 0)

                tk.Label(root, text="✅ Authorized",
                         font=("bold", 25), bg="green").place(x=450, y=400)

            else:
                # ❌ UNAUTHORIZED
                text = "Unauthorized"
                color = (0, 0, 255)

                tk.Label(root, text="❌ Unauthorized",
                         font=("bold", 25), bg="red").place(x=450, y=400)

                # Save image
                cv2.imwrite("unauthorized.jpg", img[y:y+h, x:x+w])

                # Send email
                try:
                    call(["python", "mail.py"])
                except:
                    print("Mail sending failed")

                cam.release()
                cv2.destroyAllWindows()
                ms.showwarning("Alert", "Unauthorized Person Detected! Mail Sent.")
                return

            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, text, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Camera", img)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

##############################################

def ID():
    frame = tk.LabelFrame(root, text=" --WELCOME-- ",
                          width=900, height=300,
                          font=('times', 14, 'bold'),
                          bg="pink")
    frame.place(x=400, y=100)

    tree = ttk.Treeview(frame)

    tree["columns"] = ("ID", "Name", "Last Name", "Address", "State", "Mobile")

    tree.column("#0", width=0, stretch=NO)

    for col in tree["columns"]:
        tree.column(col, anchor=CENTER, width=120)
        tree.heading(col, text=col)

    rows = my_conn.execute("SELECT * FROM User")

    count = 1
    for row in rows:
        tree.insert("", END, values=(count, row[0], row[1], row[2], row[3], row[4]))
        count += 1

    tree.pack(fill="both", expand=True)

##############################################

def registration():
    call(["python", "face_registration.py"])

def window():
    root.destroy()

##############################################
# Buttons

tk.Button(frame_alpr, text="Registration Of User",
          command=registration, width=20,
          font=('times', 15, 'bold'),
          bg="purple", fg="white").place(x=10, y=20)

tk.Button(frame_alpr, text="Display",
          command=ID, width=20,
          font=('times', 15, 'bold'),
          bg="purple", fg="white").place(x=10, y=80)

tk.Button(frame_alpr, text="Create Face Data",
          command=Create_database, width=15,
          font=('times', 15, 'bold'),
          bg="purple", fg="white").place(x=10, y=140)

tk.Button(frame_alpr, text="Train Face Data",
          command=Train_database, width=20,
          font=('times', 15, 'bold'),
          bg="purple", fg="white").place(x=10, y=200)

tk.Button(frame_alpr, text="Face Authentication",
          command=Test_database, width=20,
          font=('times', 15, 'bold'),
          bg="purple", fg="white").place(x=10, y=260)

entry2 = tk.Entry(frame_alpr, bd=5, width=7)
entry2.place(x=210, y=150)

tk.Button(frame_alpr, text="Exit",
          command=window, width=20,
          font=('times', 15, 'bold'),
          bg="red", fg="white").place(x=10, y=320)

##############################################
root.mainloop()