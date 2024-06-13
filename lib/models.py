# lib/db/models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "sqlite:///personal_finance_tracker.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association table for many-to-many relationship between Transactions and Categories
transaction_categories = Table('transaction_categories', Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transactions.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    accounts = relationship('Account', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, index=True, nullable=False)
    type = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    user = relationship('User', back_populates='transactions')
    account = relationship('Account', back_populates='transactions')
    categories = relationship('Category', secondary=transaction_categories, back_populates='transactions')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    transactions = relationship('Transaction', secondary=transaction_categories, back_populates='categories')

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_name = Column(String)
    amount = Column(Float)
    user = relationship('User', back_populates='budgets') 

Base.metadata.create_all(bind=engine)
