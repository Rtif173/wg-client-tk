import tkinter as tk
from tkinter import simpledialog

def get_password():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Use simpledialog to create a password prompt
    password = simpledialog.askstring("Password", "Enter your password:", show='*')

    return password

if __name__ == "__main__":
    password = get_password()
    print(password)