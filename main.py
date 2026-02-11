import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess

# Database Connection
def initialize_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

initialize_db()

def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    
    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful! You can now login.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    conn.close()

def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Success", "Login Successful!")
        root.destroy()
        open_home()
    else:
        messagebox.showerror("Error", "Invalid Username or Password!")

def open_home():
    home = tk.Tk()
    home.title("Expense Splitter Application")
    home.geometry("400x500")
    home.configure(bg="#D4F1F4")
    
    tk.Label(home, text="Expense Splitter Application", font=("Arial", 14, "bold"), bg="#D4F1F4").pack(pady=10)
    
    def open_user_registration():
        subprocess.Popen(["python", "user_registration.py"])

    def open_expense_entry():
        import expense_entry
        expense_entry.launch_expense_entry()

    def open_group_expense():
        import group_expense_calculation
        group_expense_calculation.launch_expense_entry

    def open_balance_settlement():
        import balance_settlement
        balance_settlement.launch_balance_settlement()
    
    # Buttons for Navigating Modules
    tk.Button(home, text="Expense Entry", command=open_expense_entry, bg="#75E6DA", fg="white").pack(pady=5)
    tk.Button(home, text="Group Expense Calculation", command=open_group_expense, bg="#75E6DA", fg="white").pack(pady=5)
    tk.Button(home, text="Balance Settlement", command=open_balance_settlement, bg="#75E6DA", fg="white").pack(pady=5)
    
    tk.Button(home, text="Exit", command=home.quit, bg="#05445E", fg="white").pack(pady=10)
    
    home.mainloop()

# Main Login & Register Window
root = tk.Tk()
root.title("Login & Register")
root.geometry("600x300")
root.configure(bg="#189AB4")

# Frames for Login & Register
login_frame = tk.Frame(root, bg="#D4F1F4")
login_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
register_frame = tk.Frame(root, bg="#75E6DA")
register_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Login Section
tk.Label(login_frame, text="Login", font=("Arial", 14, "bold"), bg="#D4F1F4").pack(pady=10)
tk.Label(login_frame, text="Username:", bg="#D4F1F4").pack()
login_username_entry = tk.Entry(login_frame)
login_username_entry.pack()
tk.Label(login_frame, text="Password:", bg="#D4F1F4").pack()
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.pack()
tk.Button(login_frame, text="Login", command=login_user, bg="#05445E", fg="white").pack(pady=10)

# Register Section
tk.Label(register_frame, text="Register", font=("Arial", 14, "bold"), bg="#75E6DA").pack(pady=10)
tk.Label(register_frame, text="Username:", bg="#75E6DA").pack()
reg_username_entry = tk.Entry(register_frame)
reg_username_entry.pack()
tk.Label(register_frame, text="Password:", bg="#75E6DA").pack()
reg_password_entry = tk.Entry(register_frame, show="*")
reg_password_entry.pack()
tk.Button(register_frame, text="Register", command=register_user, bg="#05445E", fg="white").pack(pady=10)

root.mainloop()
