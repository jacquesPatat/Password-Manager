from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import os
import re
from cryptography.fernet import Fernet

# ---------------------------- ENCRYPTION ------------------------------- #

KEY_FILE = "key.key"
DATA_FILE = "data.json"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

fernet = load_key()

def encrypt_data(data: dict):
    json_data = json.dumps(data).encode()
    encrypted = fernet.encrypt(json_data)
    with open(DATA_FILE, "wb") as file:
        file.write(encrypted)

def decrypt_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "rb") as file:
        encrypted = file.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except Exception:
        messagebox.showerror(title="Error", message="Failed to decrypt or decode data file.")
        return {}

# ---------------------------- PASSWORD STRENGTH ------------------------------- #

def get_password_strength(password):
    length = len(password)
    has_upper = re.search(r'[A-Z]', password)
    has_lower = re.search(r'[a-z]', password)
    has_digit = re.search(r'[0-9]', password)
    has_symbol = re.search(r'[^a-zA-Z0-9]', password)

    score = sum(bool(x) for x in [has_upper, has_lower, has_digit, has_symbol])

    if length >= 12 and score == 4:
        return "Strong", "green"
    elif length >= 8 and score >= 3:
        return "Medium", "orange"
    else:
        return "Weak", "red"

def update_strength_label(*args):
    password = password_entry.get()
    strength, color = get_password_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = list('0123456789')
    symbols = list('!#$%&()*+')

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    update_strength_label()

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if not website or not password:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        return

    data = decrypt_data()
    data.update(new_data)
    encrypt_data(data)

    website_entry.delete(0, END)
    password_entry.delete(0, END)
    strength_label.config(text="Strength:")

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().strip()
    data = decrypt_data()
    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Not found", message=f"No details for '{website}' exist.")

# ---------------------------- CLEAR FIELDS ------------------------------- #
def clear_fields():
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)
    strength_label.config(text="Strength:")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.resizable(False, False)

canvas = Canvas(height=200, width=200)
try:
    logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)
except:
    canvas.create_text(100, 100, text="No Logo", fill="red", font=("Arial", 14))
canvas.grid(row=0, column=1)

# Labels
Label(text="Website:").grid(row=1, column=0)
Label(text="Email/Username:").grid(row=2, column=0)
Label(text="Password:").grid(row=3, column=0)

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)
password_entry.bind("<KeyRelease>", update_strength_label)

# Strength feedback
strength_label = Label(text="Strength:")
strength_label.grid(row=4, column=1, sticky="w")

# Buttons
Button(text="Search", width=13, command=find_password).grid(row=1, column=2)
Button(text="Generate Password", command=generate_password).grid(row=3, column=2)
Button(text="Add", width=36, command=save).grid(row=5, column=1, columnspan=2)
Button(text="Clear", width=36, command=clear_fields).grid(row=6, column=1, columnspan=2)

window.mainloop()
