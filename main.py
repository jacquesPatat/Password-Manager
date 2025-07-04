from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import string
import os

# ---------------------------- CONSTANTS ------------------------------- #
DATA_FILE = "data.txt"
LOGO_FILE = "logo.png"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generate a random secure password and insert it into the entry field."""
    letters = list(string.ascii_letters)
    numbers = list(string.digits)
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

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Save website, email, and password info into a local file after validation."""
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not password:
        messagebox.showinfo(title="Missing Information", message="Please fill out all fields (website and password).")
        return

    is_ok = messagebox.askokcancel(
        title=website,
        message=f"These are the details entered:\nEmail: {email}\nPassword: {password}\nSave entry?"
    )

    if is_ok:
        with open(DATA_FILE, "a", encoding="utf-8") as data_file:
            data_file.write(f"{website} | {email} | {password}\n")
        website_entry.delete(0, END)
        password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Load logo safely
canvas = Canvas(height=200, width=200)
if os.path.exists(LOGO_FILE):
    logo_img = PhotoImage(file=LOGO_FILE)
    canvas.create_image(100, 100, image=logo_img)
else:
    canvas.create_text(100, 100, text="Logo Not Found", fill="red", font=("Arial", 14))
canvas.grid(row=0, column=1)

# Labels
Label(text="Website:").grid(row=1, column=0)
Label(text="Email/Username:").grid(row=2, column=0)
Label(text="Password:").grid(row=3, column=0)

# Entry fields
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
Button(text="Generate Password", command=generate_password).grid(row=3, column=2)
Button(text="Add", width=36, command=save).grid(row=4, column=1, columnspan=2)

window.mainloop()
