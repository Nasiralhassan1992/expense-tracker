"""
Expense Tracker Application

A simple command-line expense tracker built with Python and SQLite.

Features:
- Add, view, update, and delete expenses
- Filter by category and date
- Monthly and category summaries

Author: Nasir Alhassan
"""

import sqlite3
from datetime import datetime

# ==============================
# DATABASE SETUP
# ==============================

conn = sqlite3.connect("my_expenses.db")
cursor = conn.cursor()


def setup_db():
    """Create the expenses table if it does not exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)
    conn.commit()


# ==============================
# INPUT VALIDATION FUNCTIONS
# ==============================

def get_float(prompt):
    """Safely get a positive float input from user."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Amount cannot be negative!")
                continue
            return value
        except ValueError:
            print("Please enter a valid number!")


def get_int(prompt):
    """Safely get an integer input from user."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number!")


def get_text(prompt):
    """Safely get non-empty text input."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty!")
        else:
            return value


def get_date():
    """Get a valid date (YYYY-MM-DD) or default to today."""
    while True:
        date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date_input:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format! Use YYYY-MM-DD.")


# ==============================
# EXPENSE OPERATIONS (CRUD)
# ==============================

def add_expense():
    """Add a new expense to the database."""
    try:
        date = get_date()
        category = get_text("Enter category: ")
        amount = get_float("Enter amount: ")

        cursor.execute("""
            INSERT INTO expenses (date, category, amount)
            VALUES (?, ?, ?)
        """, (date, category, amount))

        conn.commit()
        print("Expense added successfully!")

    except Exception as e:
        print(f"Error adding expense: {e}")


def view_expenses():
    """Display all expenses."""
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    print("\n--- All Expenses ---")
    if not rows:
        print("No expenses found.")
        return

    for row in rows:
        print(f"ID: {row[0]} | Date: {row[1]} | Category: {row[2]} | ₦{row[3]:.2f}")


def delete_expense():
    """Delete an expense by ID."""
    try:
        exp_id = get_int("Enter expense ID to delete: ")

        cursor.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
        conn.commit()

        if cursor.rowcount == 0:
            print("No expense found with that ID.")
        else:
            print("Expense deleted successfully.")

    except Exception as e:
        print(f"Error deleting expense: {e}")


def update_expense():
    """Update an existing expense."""
    try:
        expense_id = get_int("Enter expense ID: ")
        date = get_date()
        category = get_text("Enter new category: ")
        amount = get_float("Enter new amount: ")

        cursor.execute("""
            UPDATE expenses
            SET date = ?, category = ?, amount = ?
            WHERE id = ?
        """, (date, category, amount, expense_id))

        if cursor.rowcount == 0:
            print("No expense found with that ID.")
        else:
            conn.commit()
            print("Expense updated successfully!")

    except Exception as e:
        print(f"Error updating expense: {e}")


# ==============================
# FILTERING FUNCTIONS
# ==============================

def filter_by_category():
    """Filter expenses by category."""
    try:
        category = get_text("Enter category to filter: ")

        cursor.execute("""
            SELECT * FROM expenses
            WHERE category LIKE ?
        """, (f"%{category}%",))

        rows = cursor.fetchall()

        print(f"\n--- Expenses for '{category}' ---")
        if not rows:
            print("No expenses found.")
            return

        for row in rows:
            print(f"ID: {row[0]} | Date: {row[1]} | Category: {row[2]} | ₦{row[3]:.2f}")

    except Exception as e:
        print(f"Error filtering by category: {e}")


def filter_by_date():
    """Filter expenses by date."""
    try:
        date = get_text("Enter date (YYYY-MM or YYYY-MM-DD): ")

        cursor.execute("""
            SELECT * FROM expenses
            WHERE date LIKE ?
        """, (f"{date}%",))

        rows = cursor.fetchall()

        print(f"\n--- Expenses for '{date}' ---")
        if not rows:
            print("No expenses found.")
            return

        for row in rows:
            print(f"ID: {row[0]} | Date: {row[1]} | Category: {row[2]} | ₦{row[3]:.2f}")

    except Exception as e:
        print(f"Error filtering by date: {e}")


# ==============================
# REPORTING FUNCTIONS
# ==============================

def total_expenses():
    """Calculate total expenses."""
    try:
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0
        print(f"\nTotal spending: ₦{total:.2f}")
        return total

    except Exception as e:
        print(f"Error calculating total: {e}")
        return 0


def get_month_total():
    """Calculate total expenses for a specific month."""
    try:
        month = get_text("Enter month (YYYY-MM): ")

        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE date LIKE ?
        """, (f"{month}%",))

        total = cursor.fetchone()[0]

        if total:
            print(f"\nTotal for {month}: ₦{total:.2f}")
        else:
            print(f"No expenses found for {month}.")

    except Exception as e:
        print(f"Error calculating monthly total: {e}")


def get_category_summary():
    """Display spending summary by category."""
    try:
        cursor.execute("""
            SELECT category, SUM(amount), COUNT(*)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)

        results = cursor.fetchall()

        print("\n--- Spending Summary by Category ---")
        print(f"{'Category':<15} | {'Total':<10} | Items")
        print("-" * 40)

        for category, total, count in results:
            print(f"{category:<15} | ₦{total:<10.2f} | {count}")

    except Exception as e:
        print(f"Error generating summary: {e}")


# ==============================
# CLOSE DATABASE
# ==============================

def close_db():
    """Close database connection."""
    try:
        conn.close()
        print("Database closed.")
    except Exception as e:
        print(f"Error closing database: {e}")