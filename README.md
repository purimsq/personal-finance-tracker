## Personal Finance Tracker
# Introduction
The Personal Finance Tracker is a simple command-line interface (CLI) application to help you manage your personal finances. You can register, log in, add accounts, record transactions, generate reports, and set and track budget goals.

# Features
- User Registration and Login: Securely register and log in.
- Account Management: Add and manage accounts.
- Transaction Recording: Record transactions with details like date, amount, and description.
- Financial Summaries: Generate and view financial summaries.
- Budget Management: Set and track budget goals.

## Technologies Used
- Python: Programming language.
- SQLAlchemy: Database interactions.
- Alembic: Database migrations.
- SQLite: Database for storing information.

## Project Structure

personal-finance-tracker/
├── alembic/                 # Database migrations
├── lib/
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py        # Database models
│   │   └── database.py      # Database setup
│   └── utils.py             # Utility functions
├── cli.py                   # CLI logic
├── app.py                   # Main entry point
├── Pipfile                  # Pipenv dependencies
├── Pipfile.lock             # Pipenv lock file
└── README.md                # Project README
## Setup Instructions
# Prerequisites
Python 3.6+
Pipenv
# Installation
Clone the repository:

git clone https://github.com/yourusername/personal-finance-tracker.git
cd personal-finance-tracker

Install dependencies:
pipenv install

Set up the database:
alembic upgrade head
Usage

Activate the Pipenv shell:
pipenv shell

Run the application:
# Copy code
python app.py
Follow the CLI prompts to:

# Register or log in

Add accounts and transactions
Generate financial summaries
Set and track budget goals
Database Models

# User

id: Integer, Primary Key
username: String, Unique
email: String, Unique
password: String (hashed)

# Account

id: Integer, Primary Key
user_id: Integer, Foreign Key
name: String
type: String (e.g., checking, savings)
balance: Float

# Transaction

id: Integer, Primary Key
user_id: Integer, Foreign Key
account_id: Integer, Foreign Key
amount: Float
date: String (YYYY-MM-DD)
description: String

# Category

id: Integer, Primary Key
name: String

## Budget

id: Integer, Primary Key
user_id: Integer, Foreign Key
category_name: String
**
markdown
Copy code
amount**: Float

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License. 






