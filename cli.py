import getpass
from lib.db.models import Base, User, Account, Transaction, Category
from lib.utils import hash_password, check_password
import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///personal_finance_tracker.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def register(session):
    username = input("Username: ")
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    hashed_password = hash_password(password)

    user = User(username=username, email=email, password=hashed_password)
    session.add(user)
    session.commit()
    print("User registered successfully!")

def login(session):
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    user = session.query(User).filter_by(username=username).first()
    if user and check_password(password, user.password):
        print("Login successful!")
        return user
    else:
        print("Invalid username or password.")
        return None

def add_account(session, user):
    name = input("Account name: ")
    account_type = input("Account type (checking/savings): ")
    balance = float(input("Initial balance: "))

    account = Account(user_id=user.id, name=name, type=account_type, balance=balance)
    session.add(account)
    session.commit()
    print("Account added successfully!")

def delete_account(session, user):
    account_name = input("Account name to delete: ")
    account_name_lower = account_name.lower()  # Convert to lower case for case insensitivity
    account = session.query(Account).filter_by(user_id=user.id).filter(func.lower(Account.name) == account_name_lower).first()
    if not account:
        print("Account deleted successfully.")
        return

    # Delete all transactions associated with the account
    transactions = session.query(Transaction).filter_by(account_id=account.id).all()
    for transaction in transactions:
        session.delete(transaction)

    # Delete the account itself
    session.delete(account)
    session.commit()
    print(f"Account '{account_name}' and associated transactions deleted successfully!")

def add_transaction(session, user):
    account_name = input("Account name: ")
    account = session.query(Account).filter_by(user_id=user.id, name=account_name).first()
    if not account:
        print("Account not found.")
        return

    amount = float(input("Transaction amount: "))
    date = input("Transaction date (YYYY-MM-DD): ")
    description = input("Description: ")

    transaction = Transaction(
        user_id=user.id, 
        account_id=account.id, 
        amount=amount, 
        date=datetime.datetime.strptime(date, '%Y-%m-%d'), 
        description=description
    )
    session.add(transaction)
    session.commit()
    print("Transaction added successfully!")

def create_financial_summary(session, user):
    print("Creating financial summary...")

    transactions = session.query(Transaction).filter_by(user_id=user.id).all()

    summary = {}
    for transaction in transactions:
        month = transaction.date.strftime('%Y-%m')
        if month not in summary:
            summary[month] = {'income': 0, 'expenses': 0}
        if transaction.amount >= 0:
            summary[month]['income'] += transaction.amount
        else:
            summary[month]['expenses'] += abs(transaction.amount)

    print("Financial summary created successfully!")
    for month, data in summary.items():
        print(f"{month}: Income = {data['income']}, Expenses = {data['expenses']}")

def view_generated_reports(session, user):
    print("Displaying generated reports...")
    create_financial_summary(session, user)

def generate_report(session, user):
    while True:
        print("\nGenerate Report Menu")
        print("1. Create Financial Summary")
        print("2. View Generated Reports")
        print("3. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            create_financial_summary(session, user)
        elif choice == '2':
            view_generated_reports(session, user)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def update_user_account(session, user):
    print("\nUpdate Account Information")
    new_username = input("New username (leave blank to keep current): ")
    new_password = getpass.getpass("New password (leave blank to keep current): ")

    if new_username:
        user.username = new_username
    if new_password:
        user.password = hash_password(new_password)
    
    session.commit()
    print("Account information updated successfully!")

def main_menu(session):
    print("Welcome to the Personal Finance Tracker!")
    user = None

    while True:
        if not user:
            print("\n1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                register(session)
            elif choice == '2':
                user = login(session)
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("\nMain Menu")
            print("1. Add Account")
            print("2. Add Transaction")
            print("3. Generate Report")
            print("4. Update Account Information")
            print("5. Delete Account")
            print("6. Logout")
            print("7. Exit")

            choice = input("Choose an option: ")

            if choice == '1':
                add_account(session, user)
            elif choice == '2':
                add_transaction(session, user)
            elif choice == '3':
                generate_report(session, user)
            elif choice == '4':
                update_user_account(session, user)
            elif choice == '5':
                delete_account(session, user)
            elif choice == '6':
                print("Logging out...")
                user = None
            elif choice == '7':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        main_menu(session)
