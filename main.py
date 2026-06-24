import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc
import datetime
import time
import os


# Maximum number of password attempts allowed
MAX_PASSWORD_ATTEMPTS = 3
def exit():
    reply=messagebox.askyesno('Confirmation','Are you sure you want to exit?')
    if reply:
        time.sleep(2)
        root.destroy()
    else:
        pass


def check():
    root.withdraw()
    if os.path.exists('password.txt'):
        with open('password.txt', "r") as file:
            lines = file.readlines()
            if lines:
                enter_password()
            else:
                create_user()
    else:
        create_user()



def create_password_file():
    if not os.path.exists('password.txt'):
        with open('password.txt', "w") as file:
            pass  # Empty file


def create_user():
    def confirm():
            if var_Uc.get() != "" and var_Pc.get() != "":
                with open('password.txt', "a") as file:
                    file.write(f"{var_Uc.get()}:{var_Pc.get()}\n")
                    messagebox.showinfo("CONFIRMED", "User created successfully.")
                    create_window.destroy()
                    enter_password()
            else:
                messagebox.showerror("ERROR", "Please enter both username and password.")
    create_password_file()
    global create_window
    create_window = tk.Toplevel(root)
    create_window.title("Create User")
    create_window.config(bg="light blue")
    create_window.maxsize(450, 130)
    create_window.minsize(440, 130)

    l3 = tk.Label(create_window, text="Enter Username", bg="light blue", fg="black", width=20)
    l3.grid(row=0, column=0, padx=10, pady=10)
    l3.config(font=("Ariel",12))
    l4 = tk.Label(create_window, text="Enter Password", bg="light blue", fg="black", width=20)
    l4.grid(row=1, column=0, padx=10, pady=10)
    l4.config(font=("Ariel",12))
    # for username
    global var_Uc
    var_Uc = tk.StringVar()

    # for password
    global var_Pc
    var_Pc = tk.StringVar()

    e1 = tk.Entry(create_window, textvariable=var_Uc, bg="white", fg="black", width=20)
    e1.grid(row=0, column=1, padx=10, pady=10)
    e1.config(font=("Impact,12"))
    e2 = tk.Entry(create_window, textvariable=var_Pc, bg="white", fg="black", width=20)
    e2.grid(row=1, column=1, padx=10, pady=10)
    e2.config(font=("Impact,12"))
    b3 = tk.Button(create_window, text="CONFIRM", bg="green", fg="black", width=20, command=confirm)
    b3.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
    b3.config(font=("Garamond",10,"bold"))

    # Update the variable p whenever the entry changes
    var_Uc.trace_add('write', lambda *args: update_Uc(var_Uc.get()))
    var_Pc.trace_add('write', lambda *args: update_Pc(var_Pc.get()))


def add():
    data_window.destroy()
    create_user()


def enter_password():
    def check_password():
        # Counter to keep track of password attempts
        attempts = 0

        # Open the password file and iterate through each line
        with open('password.txt', "r") as file:
            for line in file:
                # Split the line into username and password
                username, password = line.strip().split(":")

                # Check if the entered username and password match the current line
                if var_Ue.get() == username and var_Pe.get() == password:
                    # If a match is found, grant access and return
                    enter_window.destroy()
                    messagebox.showinfo("ACCESS GRANTED", "Welcome User")
                    data()
                    return

            # If no match is found, increment the attempts counter
            attempts += 1

            # Check if the maximum number of attempts has been reached
            if attempts >= MAX_PASSWORD_ATTEMPTS:
                # If maximum attempts reached, display an error message and exit
                enter_window.destroy()
                messagebox.showinfo("ACCESS DENIED", "Maximum password attempts reached. Exiting...")
                time.sleep(2)
                root.destroy()
            else:
                # If maximum attempts not reached, display an error message with remaining attempts
                messagebox.showinfo("ACCESS DENIED", f"Incorrect username or password. {MAX_PASSWORD_ATTEMPTS - attempts} attempts remaining.")



    global enter_window
    enter_window = tk.Toplevel(root)
    enter_window.title("Enter Credentials")
    enter_window.config(bg="light blue")
    enter_window.maxsize(450, 130)
    enter_window.minsize(450, 130)
    l3 = tk.Label(enter_window, text="Enter Username", bg="light blue", fg="black", width=20)
    l3.grid(row=0, column=0, padx=10, pady=10)
    l3.config(font=("Ariel",12))
    l4 = tk.Label(enter_window, text="Enter Password", bg="light blue", fg="black", width=20)
    l4.grid(row=1, column=0, padx=10, pady=10)
    l4.config(font=("Ariel",12))
    # for entry username
    global var_Ue
    var_Ue = tk.StringVar()
    # for entry password
    global var_Pe
    var_Pe = tk.StringVar()
    e1 = tk.Entry(enter_window, textvariable=var_Ue, bg="white", fg="black", width=20)
    e1.grid(row=0, column=1, padx=10, pady=10)
    e1.config(font=("Impact,12"))
    e2 = tk.Entry(enter_window, textvariable=var_Pe, bg="white", fg="black", width=20)
    e2.grid(row=1, column=1, padx=10, pady=10)
    e2.config(font=("Impact,12"))

    b3 = tk.Button(enter_window, text="CONFIRM", bg="green", fg="black", width=20, command=check_password)
    b3.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
    b3.config(font=("Garamond",10,"bold"))

    # Update the variables whenever the entry changes
    var_Ue.trace_add('write', lambda *args: update_Ue(var_Ue.get()))
    var_Pe.trace_add('write', lambda *args: update_Pe(var_Pe.get()))


def edit():
    con = pyodbc.connect(
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ="C:Database1.accdb";')
    var1 = StringVar()
    var2 = StringVar()
    var3 = StringVar()
    var4 = StringVar()
    var5 = StringVar()

    def insert():
        c1 = con.cursor()
        c1.execute(f"INSERT INTO BankData(Customername,Nameofchannel,Commencementdate,Requestdate,Region,Units)"
                   f"VALUES ('{var1.get()}','{combo_box1.get()}' '{var2.get()}', '{var3.get()}', '{var4.get()}','{combo_box2.get()}')")
        con.commit()
        data()
        messagebox.showinfo("Success", "Record inserted successfully!")

    def delete():
        c1 = con.cursor()
        c1.execute(f"DELETE FROM BankData where Customername='{var5.get()}'")
        con.commit()
        data()
        messagebox.showinfo("success", "One record has been successfully deleted")

    def open_data_window():
        edit_window.destroy()
        messagebox.showinfo("SUCCESS", "Your request has been processed.")
        data()

    def on_select():
        selected_category1 = combo_box1.get()
        selected_category2 = combo_box2.get()
        print("Selected category:", selected_category1)
        print("Selected category:", selected_category2)

    edit_window = tk.Toplevel(root)
    edit_window.title("EDIT DATA")
    edit_window.config(bg="light blue")
    edit_window.maxsize(320, 550)
    edit_window.minsize(320, 550)
    labels = [
        "Customer Name", "Name of channel", "Commencement Date",
        "Request Date", "Region", "Units"
    ]
    for i, label_text in enumerate(labels):
        label = Label(edit_window, text=label_text, bg="white", fg="black", width=20)
        label.grid(row=i+1, column=0, padx=10, pady=20)

    # Define the categories
    channel = ["FBL-Bancassurance", "MCB-Bancassurance", "Agency", "Silk Bank","WMF-Bancassurance","OTHER"]
    regions = ["CENTRAL REGION", "EAST REGION", "WEST REGION", "NORTH REGION","SOUTH REGION", "Karachi","OTHER"]

    # Create a Combobox widget
    combo_box1 = ttk.Combobox(edit_window, values=channel, width=20)
    combo_box1.grid(row=2, column=1, padx=10, pady=20)
    combo_box2 = ttk.Combobox(edit_window, values=regions, width=20)
    combo_box2.grid(row=5, column=1, padx=10, pady=20)

    # Set the initial value
    combo_box1.set("Select Category")
    combo_box2.set("Select Category")

    # Bind the selection event
    combo_box1.bind("<<ComboboxSelected>>", on_select)
    combo_box2.bind("<<ComboboxSelected>>", on_select)

    e3 = Entry(edit_window, textvariable=var1, bg="white", fg="black", width=20)
    e3.grid(row=1, column=1, padx=10, pady=20)
    e4 = Entry(edit_window, textvariable=var2, bg="white", fg="black", width=20)
    e4.grid(row=3, column=1, padx=10, pady=20)
    e5 = Entry(edit_window, textvariable=var3, bg="white", fg="black", width=20)
    e5.grid(row=4, column=1, padx=10, pady=20)
    e6 = Entry(edit_window, textvariable=var4, bg="white", fg="black", width=20)
    e6.grid(row=6, column=1, padx=10, pady=20)
    e7 = Entry(edit_window, textvariable=var5, bg="white", fg="black", width=20)
    e7.grid(row=9, column=0, padx=10, pady=20)

    b1 = Button(edit_window, text="display", bg="blue", fg="white", width=12, command=open_data_window)
    b1.grid(row=11, column=0, padx=10, pady=10)
    b2 = Button(edit_window, text="add record", bg="green", fg="white", width=12, command=insert)
    b2.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    b3 = Button(edit_window, text="delete record", bg="red", fg="white", width=12, command=delete)
    b3.grid(row=9, column=1, padx=10, pady=10)
    b5 = tk.Button(edit_window, text="EXIT", bg="black", fg="red", width=10, command=exit)
    b5.grid(row=11, column=1, padx=10, pady=10)


def data():
    con = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                         r'DBQ="C:\Users\Sony\Documents\Database1.accdb";')

    def display():
        query = f'SELECT  Customername, Nameofchannel,Commencementdate, Requestdate, Region, Units FROM BankData'
        cursor = con.cursor()
        cursor.execute(query)
        cursor3 = cursor.fetchall()
        for data in cursor3:
            formatted_data = [d.strftime('%d-%m-%Y') if isinstance(d, datetime.date) else d for d in data]
            stable.insert('', END, values=formatted_data)

    def search():
        con = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                             r'DBQ="C:\Users\Sony\Documents\Database1.accdb";')
        cursor = con.cursor()
        query = f"SELECT Customername, Nameofchannel, Commencementdate, Requestdate, Region, Units FROM BankData WHERE Customername LIKE '%{var_search.get()}%'"
        cursor.execute(query)
        records = cursor.fetchall()
        stable.delete(*stable.get_children())
        for record in records:
            formatted_data = [d.strftime('%d-%m-%Y') if isinstance(d, datetime.date) else d for d in record]
            stable.insert('', 'end', values=formatted_data)

    def edit_data():
        data_window.destroy()
        messagebox.showinfo("ALERT", "Please note that data changed will be set and can only be changed if the entry is manually deleted again.")
        edit()
    global data_window
    data_window = tk.Toplevel(root)
    data_window.title("INSURANCE RECORD")
    f = Frame(data_window, bg="light blue")
    f.place(x=0, y=520, width=1400, height=200)
    b1 = Button(f, text="DISPLAY", bg="blue", fg="white", width=20, command=display)
    b1.grid(row=1, column=0, padx=10, pady=10)
    b1.config(font=("Garamond",12,"bold"))
    # Search bar
    l_search = tk.Label(f, text="SEARCH CLIENT:", bg="green", fg="black", width=20)
    l_search.grid(row=1, column=1, padx=10, pady=10)
    l_search.config(font=("Garamond",12,"bold"))
    var_search = tk.StringVar()
    e_search = tk.Entry(f, textvariable=var_search, bg="white", fg="black", width=20)
    e_search.grid(row=2, column=1, padx=10, pady=5)
    b_search = tk.Button(f, text="SEARCH", bg="blue", fg="white", width=20, command=search)
    b_search.grid(row=3, column=1, padx=10, pady=5)
    b_search.config(font=("Garamond",12,"bold"))
    b_edit = tk.Button(f, text="EDIT", bg="green", fg="black", width=20, command=edit_data)
    b_edit.grid(row=2, column=0, padx=10, pady=5)
    b_edit.config(font=("Garamond",12,"bold"))
    b_exit= tk.Button(f, text="EXIT", bg="red", fg="black", width=20, command=exit)
    b_exit.grid(row=3, column=0, padx=10, pady=5)
    b_exit.config(font=("Garamond",12,"bold"))
    b_add= tk.Button(f, text="Add new user", bg="white", fg="black", width=20, command=add)
    b_add.grid(row=1, column=2, padx=10, pady=5)
    b_add.config(font=("Garamond",10,"bold"))
    label1 = Label(data_window, text="SURRENDER REPORT", bg="white", fg="black")
    label1.grid(row=0, column=0)
    b_edit.config(font=("Garamond",12,"bold"))

    f2 = Frame(data_window, bg="light blue")
    f2.place(x=0, y=20, width=1400, height=500)
    # Create a style for the Treeview
    style = ttk.Style(root)

    # Set the style for the Treeview
    style.theme_use("default")  # Use the default theme

    # Define the colors for the Treeview
    style.configure("Treeview",
                    background="white",  # Background color
                    foreground="black",  # Text color
                    fieldbackground="white")  # Background color for the entry field

    stable = ttk.Treeview(f2, height=650,columns=( "Customername", "Nameofchannel","Commencementdate", "Requestdate", "Region", "Units"), show="headings")
    stable.heading("Customername", text="Customer Name")
    stable.heading("Nameofchannel", text="Name of Channel")
    stable.heading("Commencementdate", text="Commencement Date")
    stable.heading("Requestdate", text="Request Date")
    stable.heading("Region", text="Region")
    stable.heading("Units", text="Units")
    # Vertical Scrollbar
    vsb = ttk.Scrollbar(f2, orient="vertical", command=stable.yview)
    stable.configure(yscrollcommand=vsb.set)
    vsb.pack(side="left", fill="y")

    # Horizontal Scrollbar
    hsb = ttk.Scrollbar(f2, orient="horizontal", command=stable.xview)
    stable.configure(xscrollcommand=hsb.set)
    hsb.pack(side="bottom", fill="x")

    stable.pack(expand=True, fill="both")


def update_Uc(value):
    global Uc
    Uc = value


def update_Ue(value):
    global Ue
    Ue = value


def update_Pc(value):
    global Pc
    Pc = value


def update_Pe(value):
    global Pe
    Pe = value


root = tk.Tk()
root.title("INITIATION")
root.config(bg="light blue")
root.maxsize(520, 130)
root.minsize(520, 130)

l1 = tk.Label(root, text="WELCOME", bg="light blue", fg="dark green", width=20)
l1.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
l1.config(font=("Garamond",15,"bold"))

l2 = tk.Label(root, text="DO YOU WANT TO ACCESS THE CONFIDENTIAL DATA?", bg="light blue", fg="black", width=50)
l2.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
l2.config(font=("Garamond",12,"bold"))

b1 = tk.Button(root, text="YES", bg="green", fg="black", width=10, command=check)
b1.grid(row=2, column=0, padx=10, pady=10)
b1.config(font=("Garamond",10,"bold"))

b2 = tk.Button(root, text="NO", bg="red", fg="black", width=10, command=exit)
b2.grid(row=2, column=1, padx=10, pady=10)
b2.config(font=("Garamond",10,"bold"))
root.mainloop()
