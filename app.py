import sqlite3
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

# Add a transaction
def add_transaction(category, description, amount, trans_type):
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO transactions (date, category, description, amount, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), category, description, amount, trans_type))
    
    conn.commit()
    conn.close()
    print(f"{trans_type.capitalize()} added successfully!")

# View all transactions
def view_transactions():
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    
    print("\n--- Transaction History ---")
    for trans in transactions:
        print(f"ID: {trans[0]}, Date: {trans[1]}, Category: {trans[2]}, Description: {trans[3]}, Amount: {trans[4]:.2f}, Type: {trans[5]}")
    
    conn.close()

# Categorized spending
def categorized_spending():
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT category, SUM(amount) FROM transactions
        WHERE type = 'expense'
        GROUP BY category
    ''')
    spending = cursor.fetchall()
    
    print("\n--- Spending by Category ---")
    for category, total in spending:
        print(f"{category}: ${total:.2f}")
    
    conn.close()

# Monthly summary
def monthly_summary():
    month = input("Enter the month (MM): ")
    year = input("Enter the year (YYYY): ")
    
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT SUM(amount) FROM transactions
        WHERE type = 'income' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    ''', (year, month))
    income = cursor.fetchone()[0] or 0.0
    
    cursor.execute('''
        SELECT SUM(amount) FROM transactions
        WHERE type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    ''', (year, month))
    expenses = cursor.fetchone()[0] or 0.0
    
    print(f"\n--- Summary for {month}/{year} ---")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${income - expenses:.2f}")
    
    conn.close()

# Visualization: Spending by category
def visualize_spending_by_category():
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT category, SUM(amount) FROM transactions
        WHERE type = 'expense'
        GROUP BY category
    ''')
    spending = cursor.fetchall()
    
    categories = [row[0] for row in spending]
    amounts = [row[1] for row in spending]
    
    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Spending by Category")
    plt.show()
    
    conn.close()

# Visualization: Monthly income vs expenses
def visualize_monthly_summary():
    month = input("Enter the month (MM): ")
    year = input("Enter the year (YYYY): ")
    
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT SUM(amount) FROM transactions
        WHERE type = 'income' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    ''', (year, month))
    income = cursor.fetchone()[0] or 0.0
    
    cursor.execute('''
        SELECT SUM(amount) FROM transactions
        WHERE type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    ''', (year, month))
    expenses = cursor.fetchone()[0] or 0.0
    
    plt.figure(figsize=(6, 4))
    plt.bar(['Income', 'Expenses'], [income, expenses], color=['green', 'red'])
    plt.title(f"Monthly Summary for {month}/{year}")
    plt.ylabel('Amount ($)')
    plt.show()
    
    conn.close()

# Main menu
def main():
    while True:
        print("\n--- Personal Budget Tracker ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Categorized Spending")
        print("5. Monthly Summary")
        print("6. Visualize Spending by Category")
        print("7. Visualize Monthly Summary")
        print("8. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            category = input("Enter income category: ")
            description = input("Enter income description: ")
            amount = float(input("Enter amount: "))
            add_transaction(category, description, amount, 'income')
        elif choice == '2':
            category = input("Enter expense category: ")
            description = input("Enter expense description: ")
            amount = float(input("Enter amount: "))
            add_transaction(category, description, amount, 'expense')
        elif choice == '3':
            view_transactions()
        elif choice == '4':
            categorized_spending()
        elif choice == '5':
            monthly_summary()
        elif choice == '6':
            visualize_spending_by_category()
        elif choice == '7':
            visualize_monthly_summary()
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
