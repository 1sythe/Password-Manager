import tkinter as tk
from tkinter import ttk
import json
import string
import random
from cryptography.fernet import Fernet
import os

# Tkinter setup
root = tk.Tk()
root.title("Password Manager")
root.iconbitmap('icon.ico')
root.option_add("*tearOff", False)  # This is always a good idea
root.geometry("800x550")
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)
root.resizable(False, False)  # Create a style
style = ttk.Style(root)
root.tk.call("source", "proxttk-dark.tcl")
style.theme_use("proxttk-dark")

# Vars
strength = tk.IntVar()
length = tk.StringVar()
combo_list = ["How Many Symbols", "8", "9", "10", "11", "12", "13", "14"]
genpassword = ""

# Generating Fernet key if not found.
try:
    with open("key.key", "rb") as keyfile:
        key = keyfile.read()
except:
    key = Fernet.generate_key()
    with open("key.key", "wb") as keyfile:
        keyfile.write(key)
    with open("key.key", "rb") as keyfile:
        key = keyfile.read()


# ENCRYPT THE FILE

try:
    f = Fernet(key)

    with open("data.json", "rb") as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open("enc_data.json", "wb") as encrypted_file:
        encrypted_file.write(encrypted)

except:
    pass

try:
    os.remove("data.json")

except:
    pass


# Frame that holds everything
MainFrame = ttk.Frame(root, padding=(40, 0, 0, 1))
MainFrame.grid(row=0, column=1, padx=0, pady=(50, 10), sticky="nsew", rowspan=3)

# Headlline "Password Manager"
headline = ttk.Label(MainFrame, text="Password Manager", font="colortube", justify="center", foreground="white")
headline.grid(row=0, column=0, pady=10, columnspan=2)

# Info Label
InfoLabel = ttk.Label(MainFrame, text="Please enter your password to unlock the password manager.", font=("colortube", 6), justify="center", foreground="white")

# Holds json entrys
mainlist = tk.Listbox(MainFrame)

# Text box for the Entry Name (For Creating a new Entry)
Namebox = ttk.Entry(MainFrame)

# Text box for the Email
Emailbox = ttk.Entry(MainFrame)

# Text box for the Username
Userbox = ttk.Entry(MainFrame)

# Text box for the Password
Passbox = ttk.Entry(MainFrame)

# Text Box for The Password Generator
fpass = ttk.Entry(MainFrame)
fpass.insert(0, "Password...")

# Text Box for Login Page
loginpass = ttk.Entry(MainFrame)


# Insert default
Emailbox.delete(0, tk.END)
Emailbox.insert(tk.END, "Email: ")
Userbox.delete(0, tk.END)
Userbox.insert(tk.END, "Username: ")
Passbox.delete(0, tk.END)
Passbox.insert(tk.END, "Password: ")

# Combobox for Password Generator
howmanysymbols = ttk.Combobox(MainFrame, values=combo_list)
howmanysymbols.current(0)


# Buttons
loadbtn = ttk.Button(MainFrame, text="Load Selected", command=lambda: load())
deletebtn = ttk.Button(MainFrame, text="Delete Selected", command=lambda: delete())
newentrybtn = ttk.Button(MainFrame, text="Create New Entry", command=lambda: newentry())
savebtn = ttk.Button(MainFrame, text="Save New Entry", command=lambda: save())
cancelbtn = ttk.Button(MainFrame, text="cancel", command=lambda: mainmenu())
usepasswordgen = ttk.Button(MainFrame, text="Use Password Generator", command=lambda: passwordgen())
generatebutton = ttk.Button(MainFrame, text="Generate", command=lambda: random_password())
usegenpassword = ttk.Button(MainFrame, text="Use Generated Password", command=lambda: usegeneratedpassword())
loginbtn = ttk.Button(MainFrame, text="Unlock", command=lambda: checklogin())

# Radio Buttons For Password Generator
lettersonly = ttk.Radiobutton(MainFrame, text="Letters only", variable=strength, value=1)
numbersonly = ttk.Radiobutton(MainFrame, text="Numbers only", variable=strength, value=2)
lettersandnumbers = ttk.Radiobutton(MainFrame, text="Letters and numbers", variable=strength, value=3)
lettersnumbersandsymbols = ttk.Radiobutton(MainFrame, text="Letters, numbers and symbols", variable=strength, value=4)


# Get the existing data from data.json
def reload():
    with open("enc_data.json", "rb") as datafile:
        dec = f.decrypt(datafile.read())
        global data
        data = json.loads(dec)
        mainlist.delete(0, tk.END)
        for i in data["Entrys"]:
            mainlist.insert(tk.END, i)
            pass


# When starting reload the first time to get data
reload()


# Creating a new entry
def newentry():
    usepasswordgen.grid(row=26, column=0, padx=165, pady=4, sticky="ew")
    loadbtn.grid_remove()
    deletebtn.grid_remove()
    newentrybtn.grid_remove()
    mainlist.grid_remove()
    savebtn.grid(row=27, column=0, padx=165, pady=4, sticky="ew")
    Namebox.grid(row=9, column=0, padx=150, pady=5, sticky="ew")
    cancelbtn.grid(row=30, column=0, padx=200, pady=4, sticky="ew")
    Namebox.delete(0, tk.END)
    Namebox.insert(tk.END, "Name...")
    Emailbox.delete(0, tk.END)
    Emailbox.insert(tk.END, "E-Mail...")
    Userbox.delete(0, tk.END)
    Userbox.insert(tk.END, "Username...")
    Passbox.delete(0, tk.END)
    Passbox.insert(tk.END, "Password...")


def usegeneratedpassword():
    global genpassword
    usepasswordgen.grid(row=26, column=0, padx=165, pady=4, sticky="ew")
    loadbtn.grid_remove()
    deletebtn.grid_remove()
    newentrybtn.grid_remove()
    mainlist.grid_remove()
    savebtn.grid(row=27, column=0, padx=165, pady=4, sticky="ew")
    Namebox.grid(row=9, column=0, padx=150, pady=5, sticky="ew")
    Emailbox.grid(row=10, column=0, padx=150, pady=5, sticky="ew")
    Userbox.grid(row=11, column=0, padx=150, pady=5, sticky="ew")
    Passbox.grid(row=12, column=0, padx=150, pady=5, sticky="ew")
    cancelbtn.grid(row=30, column=0, padx=200, pady=4, sticky="ew")
    usegenpassword.grid_remove()
    lettersonly.grid_remove()
    numbersonly.grid_remove()
    lettersandnumbers.grid_remove()
    lettersnumbersandsymbols.grid_remove()
    generatebutton.grid_remove()
    howmanysymbols.grid_remove()
    fpass.grid_remove()
    Passbox.delete(0, tk.END)
    Passbox.insert(tk.END, genpassword)

def mainmenu():
    InfoLabel.grid_remove()
    loginbtn.grid_remove()
    loginpass.grid_remove()
    cancelbtn.grid_remove()
    Namebox.grid_remove()
    savebtn.grid_remove()
    loadbtn.grid_remove()
    usepasswordgen.grid_remove()
    MainFrame.columnconfigure(index=0, weight=1)
    newentrybtn.grid(row=27, column=0, padx=165, pady=4, sticky="ew")
    mainlist.grid(row=3, column=0, padx=0, pady=2, sticky="ew")
    Emailbox.grid(row=10, column=0, padx=150, pady=5, sticky="ew")
    Userbox.grid(row=11, column=0, padx=150, pady=5, sticky="ew")
    Passbox.grid(row=12, column=0, padx=150, pady=5, sticky="ew")
    loadbtn.grid(row=25, column=0, padx=200, pady=4, sticky="ew")
    deletebtn.grid(row=26, column=0, padx=200, pady=4, sticky="ew")
    Emailbox.delete(0, tk.END)
    Emailbox.insert(tk.END, "Email: ")
    Userbox.delete(0, tk.END)
    Userbox.insert(tk.END, "Username: ")
    Passbox.delete(0, tk.END)
    Passbox.insert(tk.END, "Password: ")


def login():
    loginpass.grid(row=2, column=0, padx=175, pady=0, sticky="ew")
    loginbtn.grid(row=25, column=0, padx=270, pady=10, sticky="ew")
    InfoLabel.grid(row=1, column=0, pady=10, columnspan=2)

    try:
        rpass = data['Password']

    except:
        InfoLabel.configure(text="As this is your first time using\n the Passwort Manager, please set a Password.\n\nYou will use this password to unlock\nthe Password Manager.")
        loginbtn.configure(text="Set", command=lambda: setmanagerpass())


    loginpass.grid(row=2, column=0, padx=175, pady=0, sticky="ew")
    loginbtn.grid(row=25, column=0, padx=270, pady=10, sticky="ew")
    InfoLabel.grid(row=1, column=0, pady=10, columnspan=2)


def setmanagerpass():
    data['Password'] = loginpass.get()
    enc = f.encrypt(json.dumps(data).encode())
    with open("enc_data.json", "wb") as datafile:
        datafile.write(enc)
    mainmenu()


def checklogin():
    if data['Password'] == loginpass.get():
        mainmenu()
    else:
        loginpass.delete(0, tk.END)
        loginpass.insert(tk.END, "Wrong Password!")

def passwordgen():
    usegenpassword.grid(row=31, column=0, padx=270, pady=2, sticky="ew")
    lettersonly.grid(row=20, column=0, padx=270, pady=2, sticky="ew")
    numbersonly.grid(row=21, column=0, padx=270, pady=2, sticky="ew")
    lettersandnumbers.grid(row=22, column=0, padx=270, pady=2, sticky="ew")
    lettersnumbersandsymbols.grid(row=23, column=0, padx=270, pady=2, sticky="ew")
    generatebutton.grid(row=25, column=0, padx=270, pady=10, sticky="ew")
    howmanysymbols.grid(row=10, column=0, padx=250, pady=10, sticky="ew")
    fpass.grid(row=2, column=0, padx=200, pady=0, sticky="ew")
    Namebox.grid_remove()
    Emailbox.grid_remove()
    Userbox.grid_remove()
    Passbox.grid_remove()
    savebtn.grid_remove()
    cancelbtn.grid_remove()
    usepasswordgen.grid_remove()


def save():
    name = Namebox.get()
    mail = Emailbox.get()
    user = Userbox.get()
    passw = Passbox.get()
    data['Entrys'][name] = {}
    data['Entrys'][name]['Email'] = mail
    data['Entrys'][name]['Username'] = user
    data['Entrys'][name]['Password'] = passw
    with open("enc_data.json", "wb") as datafile:
        datafile.write(f.encrypt(json.dumps(data).encode()))
    mainmenu()
    reload()


# Loading Selected Entry to Text box
def load():
    s = mainlist.curselection()
    s = s[0]
    s = mainlist.get(first=s)
    Emailbox.delete(0, tk.END)
    Emailbox.insert(tk.END, "E-Mail: " + data['Entrys'][s]['Email'])
    Userbox.delete(0, tk.END)
    Userbox.insert(tk.END, "Username: " + data['Entrys'][s]['Username'])
    Passbox.delete(0, tk.END)
    Passbox.insert(tk.END, "Password: " + data['Entrys'][s]['Password'])


def delete():
    s = mainlist.curselection()
    s = s[0]
    s = mainlist.get(first=s)
    del data['Entrys'][s]
    with open("enc_data.json", "w") as datafile:
        datafile.write(f.encrypt(json.dumps(data).encode()))
    reload()


def random_password():
    global genpassword
    s = strength.get()
    if s == 1:
        symbols = string.ascii_letters
    elif s == 2:
        symbols = string.digits
    elif s == 3:
        symbols = string.ascii_letters + string.digits
    elif s == 4:
        symbols = string.ascii_letters + string.digits + string.punctuation
    else:
        fpass.delete("0", tk.END)
        fpass.insert(0, "Please Select 1 of the options")
        return

    try:
        len = int(howmanysymbols.get())

    except:
        len = 0
        fpass.delete("0", tk.END)
        fpass.insert(0, "Please choose how many symbols you want...")

    if not len == 0:
        genpassword = "".join(random.choice(symbols) for i in range(len))

        fpass.delete("0", tk.END)
        fpass.insert(0, genpassword)


login()
root.mainloop()
