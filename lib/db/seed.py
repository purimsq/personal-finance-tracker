# lib/db/seed.py
# Example seeding logic
from models import SessionLocal, User, Account, Category
session = SessionLocal()

# Add initial users, accounts, and categories
# Example:
user = User(username='testuser', email='test@example.com', password='hashed_password')
session.add(user)
session.commit()

# Don't forget to close the session
session.close()
