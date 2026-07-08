
from tkinter import *

import sqlite3
import tkinter as tk
from tkinter import messagebox as ms
from tkinter import ttk   # ✅ IMPORTANT
from PIL import Image , ImageTk     

root = Tk()
root.geometry('1500x800')
root.title("Registration Form")

# Background Image
image2 = Image.open('6.jpg')
image2 = image2.resize((1530,800), Image.LANCZOS)

background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0)

# Variables
Name = StringVar()
LastName = StringVar()
Address = StringVar()
states1 = StringVar()
Mobile = StringVar()

# ================= DATABASE =================
def database():
    name = Name.get()
    lastname = LastName.get()
    address = Address.get()
    states = states1.get()
    mobileno = Mobile.get()

    conn = sqlite3.connect('face.db')

    if (name.isdigit() or (name == "")):
        ms.showinfo("Message", "please enter valid name")

    elif (lastname.isdigit() or (lastname == "")):
        ms.showinfo("Message", "please enter valid lastname")

    elif (address == ""):
        ms.showinfo("Message", "Please Enter valid Address")

    elif (states == ""):
        ms.showinfo("Message", "Please Enter valid States")

    elif ((len(str(mobileno))) < 10 or len(str(mobileno)) > 10):
        ms.showinfo("Message", "Please Enter 10 digit mobile number")

    else:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO User (Name,Lastname,Address,States,Mobileno) VALUES(?,?,?,?,?)',
                               (name, lastname, address, states, mobileno))
                conn.commit()

            ms.showinfo('Success','User Registered Successfully')
            root.destroy()

        except Exception as e:
            ms.showerror("Database Error", str(e))

# ================= DISPLAY TABLE =================
def display():

    frame = tk.LabelFrame(root, text=" --USER DATA-- ",
                          width=900, height=250,
                          font=('times', 14, 'bold'),
                          bg="pink")
    frame.place(x=300, y=450)

    tree = ttk.Treeview(frame)

    tree["columns"] = ("ID", "Name", "Last Name", "Address", "States", "Mobile")

    tree.column("#0", width=0, stretch=NO)

    tree.column("ID", width=50, anchor=CENTER)
    tree.column("Name", width=120, anchor=CENTER)
    tree.column("Last Name", width=120, anchor=CENTER)
    tree.column("Address", width=150, anchor=CENTER)
    tree.column("States", width=100, anchor=CENTER)
    tree.column("Mobile", width=120, anchor=CENTER)

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("Address", text="Address")
    tree.heading("States", text="States")
    tree.heading("Mobile", text="Mobile")

    conn = sqlite3.connect('face.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM User")
    rows = cursor.fetchall()

    count = 1
    for row in rows:
        tree.insert("", END, values=(count, row[0], row[1], row[2], row[3], row[4]))
        count += 1

    tree.pack(fill="both", expand=True)

# ================= UI =================
Label(root, text="Registration Form",
      width=25, font=("bold", 22),
      fg="orange", bg="black").place(x=1000,y=50)

Label(root, text="Name", width=20,
      font=("bold", 15), bg='black', fg='white').place(x=1000,y=130)

Entry(root, textvar=Name, width=25).place(x=1250,y=130)

Label(root, text="Last Name", width=20,
      font=("bold", 15), bg='black', fg='white').place(x=1000,y=180)

Entry(root, textvar=LastName, width=25).place(x=1250,y=180)

Label(root, text="Address", width=20,
      font=("bold", 15), bg='black', fg='white').place(x=1000,y=230)

Entry(root, textvar=Address, width=25).place(x=1250,y=230)

Label(root, text="States", width=20,
      font=("bold", 15), bg='black', fg='white').place(x=1000,y=280)

Entry(root, textvar=states1, width=25).place(x=1250,y=280)

Label(root, text="Mobile No", width=20,
      font=("bold", 15), bg='black', fg='white').place(x=1000,y=330)

Entry(root, textvar=Mobile, width=25).place(x=1250,y=330)

Button(root, text='Submit',
       width=25, bg='red', fg='white',
       command=database).place(x=1100,y=400)

root.mainloop()