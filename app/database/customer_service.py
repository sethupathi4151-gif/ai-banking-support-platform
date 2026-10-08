from sqlalchemy import text

from app.database.connection import engine


def fetch_customer_360(customer_code: str):
    with engine.connect() as conn:

        customer = conn.execute(
            text("""
                SELECT customer_id,
                       customer_code,
                       full_name,
                       email,
                       phone,
                       risk_level,
                       created_at
                FROM customers
                WHERE customer_code = :customer_code
            """),
            {"customer_code": customer_code}
        ).mappings().first()

        if not customer:
            return None

        accounts = conn.execute(
            text("""
                SELECT account_number,
                       account_type,
                       balance,
                       status
                FROM accounts
                WHERE customer_id = :customer_id
                ORDER BY account_id
            """),
            {"customer_id": customer["customer_id"]}
        ).mappings().all()

        transactions = conn.execute(
            text("""
                SELECT t.transaction_reference,
                       t.transaction_type,
                       t.amount,
                       t.merchant_name,
                       t.transaction_status,
                       t.transaction_location,
                       t.transaction_time
                FROM transactions t
                JOIN accounts a
                    ON t.account_id = a.account_id
                WHERE a.customer_id = :customer_id
                ORDER BY t.transaction_time DESC
            """),
            {"customer_id": customer["customer_id"]}
        ).mappings().all()

        tickets = conn.execute(
            text("""
                SELECT ticket_id,
                       subject,
                       category,
                       priority,
                       risk_level,
                       status,
                       ai_confidence,
                       created_at
                FROM support_tickets
                WHERE customer_id = :customer_id
                ORDER BY created_at DESC
            """),
            {"customer_id": customer["customer_id"]}
        ).mappings().all()

        return {
            "customer": dict(customer),
            "accounts": [dict(account) for account in accounts],
            "transactions": [dict(transaction) for transaction in transactions],
            "support_tickets": [dict(ticket) for ticket in tickets]
        }