import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Setup
def setup_database():
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL)''')
    conn.commit()
    conn.close()

# Add User to Database
def add_user():
    username = entry_username.get().strip()
    if not username:
        messagebox.showwarning("Input Error", "Username cannot be empty!")
        return
    try:
        conn = sqlite3.connect("expense_splitter.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        conn.close()
        entry_username.delete(0, tk.END)
        load_users()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# Load Users from Database
def load_users():
    list_users.delete(0, tk.END)
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    conn.close()
    for user in users:
        list_users.insert(tk.END, user[0])

# Delete Selected User
def delete_user():
    selected_user = list_users.get(tk.ACTIVE)
    if not selected_user:
        messagebox.showwarning("Selection Error", "No user selected!")
        return
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (selected_user,))
    conn.commit()
    conn.close()
    load_users()

# GUI Setup
setup_database()
root = tk.Tk()
root.title("User Registration")
root.geometry("300x400")

tk.Label(root, text="Enter Username:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Button(root, text="Add User", command=add_user).pack(pady=5)

list_users = tk.Listbox(root)
list_users.pack(pady=10, fill=tk.BOTH, expand=True)

load_users()

tk.Button(root, text="Delete Selected User", command=delete_user).pack(pady=5)

root.mainloop()
