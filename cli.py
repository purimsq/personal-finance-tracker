# cli.py
import getpass
from lib.db.models import SessionLocal, User, Account, Transaction, Category
from sqlalchemy.orm import sessionmaker
from lib.utils import hash_password, check_password
import datetime

#def main_menu(sessions):

def register():
    session = SessionLocal()
    username = input("Username: ")
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    hashed_password = hash_password(password)

    user = User(username=username, email=email, password=hashed_password)
    session.add(user)
    session.commit()
    print("User registered successfully!")

def login():
    session = SessionLocal()
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    user = session.query(User).filter_by(username=username).first()
    if user and check_password(password, user.password):
        print("Login successful!")
        return user
    else:
        print("Invalid username or password.")
        return None

def add_account(user):
    session = SessionLocal()
    name = input("Account name: ")
    type = input("Account type (checking/savings): ")
    balance = float(input("Initial balance: "))

    account = Account(user_id=user.id, name=name, type=type, balance=balance)
    session.add(account)
    session.commit()
    print("Account added successfully!")

def add_transaction(user):
    session = SessionLocal()
    account_name = input("Account name: ")
    account = session.query(Account).filter_by(user_id=user.id, name=account_name).first()
    if not account:
        print("Account not found.")
        return

    amount = float(input("Transaction amount: "))
    date = input("Transaction date (YYYY-MM-DD): ")
    description = input("Description: ")

    transaction = Transaction(user_id=user.id, account_id=account.id, amount=amount, date=datetime.datetime.strptime(date, '%Y-%m-%d'), description=description)
    session.add(transaction)
    session.commit()
    print("Transaction added successfully!")

def generate_report(user):
    session = SessionLocal()
    transactions = session.query(Transaction).filter_by(user_id=user.id).all()

    print("Transactions:")
    for transaction in transactions:
        print(f"Date: {transaction.date}, Amount: {transaction.amount}, Description: {transaction.description}")

def set_budget(user):
    # Implement budget setting functionality
    pass

def cli():
    print("Welcome to the Personal Finance Tracker!")
    while True:
        print("\n1. Register\n2. Login\n3. Add Account\n4. Add Transaction\n5. Generate Report\n6. Set Budget\n7. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            register()
        elif choice == '2':
            user = login()
        elif choice == '3' and user:
            add_account(user)
        elif choice == '4' and user:
            add_transaction(user)
        elif choice == '5' and user:
            generate_report(user)
        elif choice == '6' and user:
            set_budget(user)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice or not logged in. Please try again.")

if __name__ == '__main__':
    cli()
