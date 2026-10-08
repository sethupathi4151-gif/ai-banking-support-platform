from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    customer_code = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    risk_level = Column(String(20), nullable=False, default="LOW")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    account_number = Column(String(30), unique=True, nullable=False)
    account_type = Column(String(30), nullable=False)
    balance = Column(Numeric(15, 2), nullable=False, default=0)
    status = Column(String(20), nullable=False, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    transaction_reference = Column(String(40), unique=True, nullable=False)
    transaction_type = Column(String(30), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    merchant_name = Column(String(150))
    transaction_status = Column(String(30), nullable=False)
    transaction_location = Column(String(100))
    transaction_time = Column(DateTime(timezone=True), server_default=func.now())


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    ticket_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50))
    priority = Column(String(20), nullable=False, default="LOW")
    risk_level = Column(String(20), nullable=False, default="LOW")
    status = Column(String(30), nullable=False, default="OPEN")
    ai_confidence = Column(Numeric(5, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())