import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database Setup
def setup_database():
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        amount REAL NOT NULL)''')
    conn.commit()
    conn.close()

# Add Expense to Database
def add_expense():
    description = entry_desc.get().strip()
    amount = entry_amount.get().strip()
    
    if not description or not amount:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number!")
        return
    
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (description, amount) VALUES (?, ?)", (description, amount))
    conn.commit()
    conn.close()
    entry_desc.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    load_expenses()

# Load Expenses from Database
def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, amount FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    
    for expense in expenses:
        tree.insert("", tk.END, values=(expense[0], expense[1], f"${expense[2]:.2f}"))

# Delete Selected Expense
def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "No expense selected!")
        return
    
    expense_id = tree.item(selected_item, "values")[0]
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    load_expenses()

# GUI Setup
setup_database()
root = tk.Tk()
root.title("Expense Entry")
root.geometry("400x500")
root.configure(bg="#E3FDFD")

# Form Inputs
tk.Label(root, text="Description:", bg="#E3FDFD", font=("Arial", 12)).pack(pady=5)
entry_desc = tk.Entry(root, font=("Arial", 12))
entry_desc.pack(pady=5)

tk.Label(root, text="Amount ($):", bg="#E3FDFD", font=("Arial", 12)).pack(pady=5)
entry_amount = tk.Entry(root, font=("Arial", 12))
entry_amount.pack(pady=5)

tk.Button(root, text="Add Expense", command=add_expense, bg="#71C9CE", fg="white", font=("Arial", 12, "bold"), width=15).pack(pady=5)

# Table Display
columns = ("ID", "Description", "Amount")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Description", text="Description")
tree.heading("Amount", text="Amount ($)")

tree.column("ID", width=50, anchor=tk.CENTER)
tree.column("Description", width=180)
tree.column("Amount", width=100, anchor=tk.CENTER)

tree.pack(pady=10, fill=tk.BOTH, expand=True)

load_expenses()

tk.Button(root, text="Delete Selected Expense", command=delete_expense, bg="#FF6F61", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=10)

root.mainloop()
