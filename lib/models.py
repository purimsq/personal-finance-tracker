from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    accounts = relationship('Account', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)

    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=True)

    user = relationship('User', back_populates='transactions')
    account = relationship('Account', back_populates='transactions')
    categories = relationship('TransactionCategory', back_populates)
