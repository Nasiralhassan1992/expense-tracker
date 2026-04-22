"""
Menu Interface for Expense Tracker

Handles user interaction and navigation.
"""

import os
import database_logic as db


# =============================
# HELPER FUNCTIONS
# ==============================

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pause until user presses Enter."""
    input("\nPress Enter to continue...")


def show_menu():
    """Display menu options."""
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Update Expense")
    print("5. Filter by Category")
    print("6. Filter by Date")
    print("7. Total Expenses")
    print("8. Monthly Total")
    print("9. Category Summary")
    print("10. Exit")


# ==============================
# MAIN PROGRAM
# ==============================

def main():
    """Main program loop."""
    db.setup_db()

    while True:
        clear_screen()
        show_menu()

        choice = input("Choose (1-10): ").strip()

        if choice == "1":
            db.add_expense()

        elif choice == "2":
            db.view_expenses()

        elif choice == "3":
            db.delete_expense()

        elif choice == "4":
            db.update_expense()

        elif choice == "5":
            db.filter_by_category()

        elif choice == "6":
            db.filter_by_date()

        elif choice == "7":
            db.total_expenses()

        elif choice == "8":
            db.get_month_total()

        elif choice == "9":
            db.get_category_summary()

        elif choice == "10":
            print("Closing database...")
            db.close_db()
            break

        else:
            print("Invalid choice! Please enter 1–10.")

        pause()


# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    main()
