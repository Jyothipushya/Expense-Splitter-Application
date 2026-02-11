import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database Setup
def setup_database():
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS group_expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        payer TEXT NOT NULL,
                        amount REAL NOT NULL,
                        members TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Add Group Expense to Database
def add_group_expense():
    payer = entry_payer.get().strip()
    amount = entry_amount.get().strip()
    members = entry_members.get().strip()
    
    if not payer or not amount or not members:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number!")
        return
    
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO group_expenses (payer, amount, members) VALUES (?, ?, ?)", (payer, amount, members))
    conn.commit()
    conn.close()
    entry_payer.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_members.delete(0, tk.END)
    load_group_expenses()

# Load Group Expenses from Database
def load_group_expenses():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, payer, amount, members FROM group_expenses")
    expenses = cursor.fetchall()
    conn.close()
    
    for expense in expenses:
        tree.insert("", tk.END, values=(expense[0], expense[1], f"${expense[2]:.2f}", expense[3]))

# Delete Selected Group Expense
def delete_group_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "No expense selected!")
        return
    
    expense_id = tree.item(selected_item, "values")[0]
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM group_expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    load_group_expenses()

# GUI Setup
setup_database()
root = tk.Tk()
root.title("Group Expense Calculation")
root.geometry("450x500")
root.configure(bg="#E3FDFD")

# Form Inputs
tk.Label(root, text="Payer:", bg="#E3FDFD", font=("Arial", 12)).pack(pady=5)
entry_payer = tk.Entry(root, font=("Arial", 12))
entry_payer.pack(pady=5)

tk.Label(root, text="Amount ($):", bg="#E3FDFD", font=("Arial", 12)).pack(pady=5)
entry_amount = tk.Entry(root, font=("Arial", 12))
entry_amount.pack(pady=5)

tk.Label(root, text="Members (comma separated):", bg="#E3FDFD", font=("Arial", 12)).pack(pady=5)
entry_members = tk.Entry(root, font=("Arial", 12))
entry_members.pack(pady=5)

tk.Button(root, text="Add Group Expense", command=add_group_expense, bg="#71C9CE", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

# Table Display
columns = ("ID", "Payer", "Amount", "Members")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Payer", text="Payer")
tree.heading("Amount", text="Amount ($)")
tree.heading("Members", text="Members")

tree.column("ID", width=50, anchor=tk.CENTER)
tree.column("Payer", width=100)
tree.column("Amount", width=80, anchor=tk.CENTER)
tree.column("Members", width=180)

tree.pack(pady=10, fill=tk.BOTH, expand=True)

load_group_expenses()

tk.Button(root, text="Delete Selected Expense", command=delete_group_expense, bg="#FF6F61", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)

root.mainloop()
