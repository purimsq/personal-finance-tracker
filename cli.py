import getpass
from lib.db.models import User, Account, Transaction, Category
from lib.utils import hash_password, check_password
import datetime

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

def generate_report(session, user):
    transactions = session.query(Transaction).filter_by(user_id=user.id).all()

    print("Transactions:")
    for transaction in transactions:
        print(f"Date: {transaction.date}, Amount: {transaction.amount}, Description: {transaction.description}")

def set_budget(session, user):
    # Implement budget setting functionality
    pass

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
            print("4. Set Budget")
            print("5. Logout")
            print("6. Exit")

            choice = input("Choose an option: ")

            if choice == '1':
                add_account(session, user)
            elif choice == '2':
                add_transaction(session, user)
            elif choice == '3':
                generate_report(session, user)
            elif choice == '4':
                set_budget(session, user)
            elif choice == '5':
                print("Logging out...")
                user = None
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
