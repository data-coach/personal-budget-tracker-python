import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    
    # Create a table for transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL,
            type TEXT
        )
    ''')
    conn.commit()
    conn.close()

initialize_database()

# Add transaction to database
def add_transaction(category, description, amount, trans_type):
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (date, category, description, amount, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), category, description, amount, trans_type))
    conn.commit()
    conn.close()

# GUI to add a transaction
def add_transaction_gui():
    def submit():
        category = category_entry.get()
        description = description_entry.get()
        amount = float(amount_entry.get())
        trans_type = trans_type_var.get()

        if not category or not description or not amount or not trans_type:
            messagebox.showerror("Error", "All fields are required.")
            return

        add_transaction(category, description, amount, trans_type)
        messagebox.showinfo("Success", f"{trans_type.capitalize()} added successfully!")
        window.destroy()

    window = tk.Toplevel()
    window.title("Add Transaction")
    window.geometry("400x300")

    tk.Label(window, text="Category").grid(row=0, column=0, padx=10, pady=10)
    category_entry = tk.Entry(window)
    category_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(window, text="Description").grid(row=1, column=0, padx=10, pady=10)
    description_entry = tk.Entry(window)
    description_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(window, text="Amount").grid(row=2, column=0, padx=10, pady=10)
    amount_entry = tk.Entry(window)
    amount_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(window, text="Type").grid(row=3, column=0, padx=10, pady=10)
    trans_type_var = tk.StringVar(value="income")
    trans_type_menu = ttk.Combobox(window, textvariable=trans_type_var, values=["income", "expense"])
    trans_type_menu.grid(row=3, column=1, padx=10, pady=10)

    submit_btn = tk.Button(window, text="Submit", command=submit)
    submit_btn.grid(row=4, column=0, columnspan=2, pady=20)

# View all transactions
def view_transactions():
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()

    window = tk.Toplevel()
    window.title("Transaction History")
    window.geometry("600x400")

    tree = ttk.Treeview(window, columns=("Date", "Category", "Description", "Amount", "Type"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Category", text="Category")
    tree.heading("Description", text="Description")
    tree.heading("Amount", text="Amount")
    tree.heading("Type", text="Type")

    for trans in transactions:
        tree.insert("", tk.END, values=trans[1:])
    
    tree.pack(fill=tk.BOTH, expand=True)

# Visualize spending by category
def visualize_spending_by_category():
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, SUM(amount) FROM transactions
        WHERE type = 'expense'
        GROUP BY category
    ''')
    spending = cursor.fetchall()
    conn.close()

    if not spending:
        messagebox.showinfo("Info", "No expenses to display.")
        return

    categories = [row[0] for row in spending]
    amounts = [row[1] for row in spending]

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Spending by Category")
    plt.show()

# Main GUI
def main_gui():
    root = tk.Tk()
    root.title("Personal Budget Tracker")
    root.geometry("400x300")
    
    # Set the window icon (Favicon)
    root.iconbitmap('favicon.ico')  # Provide the path to your icon file

    tk.Label(root, text="Personal Budget Tracker", font=("Helvetica", 16)).pack(pady=20)

    tk.Button(root, text="Add Transaction", width=20, command=add_transaction_gui).pack(pady=10)
    tk.Button(root, text="View Transactions", width=20, command=view_transactions).pack(pady=10)
    tk.Button(root, text="Visualize Spending", width=20, command=visualize_spending_by_category).pack(pady=10)
    tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
