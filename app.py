# app.py

from lib.db.models import SessionLocal, User, Account, Transaction, Category
from cli import main_menu

def main():
    # Set up the database session
    session = SessionLocal()

    try:
        # Run the main menu of the CLI application
        main_menu(session)
    finally:
        # Close the session when done
        session.close()

if __name__ == "__main__":
    main()
