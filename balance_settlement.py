import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from collections import defaultdict

# Function to calculate settlements
def calculate_balances():
    conn = sqlite3.connect("expense_splitter.db")
    cursor = conn.cursor()
    cursor.execute("SELECT payer, amount, members FROM group_expenses")
    expenses = cursor.fetchall()
    conn.close()
    
    balances = defaultdict(float)
    
    for payer, amount, members in expenses:
        members_list = members.split(",")
        share = amount / (len(members_list) + 1)  # Including payer
        
        balances[payer] += amount - share  # Payer's net contribution
        for member in members_list:
            member = member.strip()
            balances[member] -= share  # Member's debt
    
    return balances

# Display Settlements
def show_settlements():
    balances = calculate_balances()
    for row in tree.get_children():
        tree.delete(row)
    for user, balance in balances.items():
        if balance > 0:
            status = f"{user} should receive ${balance:.2f}"
        elif balance < 0:
            status = f"{user} owes ${-balance:.2f}"
        else:
            status = f"{user} is settled"
        
        tree.insert("", tk.END, values=(user, status))

# GUI Setup
root = tk.Tk()
root.title("Balance Settlement")
root.geometry("450x400")
root.configure(bg="#E3FDFD")

# Heading
tk.Label(root, text="Balance Settlements", bg="#E3FDFD", font=("Arial", 14, "bold")).pack(pady=5)

# Table Display
columns = ("User", "Settlement Status")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("User", text="User")
tree.heading("Settlement Status", text="Settlement Status")

tree.column("User", width=100, anchor=tk.CENTER)
tree.column("Settlement Status", width=300)

tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Button
tk.Button(root, text="Calculate Settlements", command=show_settlements, bg="#71C9CE", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

root.mainloop()
