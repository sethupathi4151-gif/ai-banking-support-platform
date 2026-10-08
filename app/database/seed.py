from sqlalchemy import text
from app.database.connection import engine


def seed_data():
    with engine.begin() as conn:

        conn.execute(text("""
    INSERT INTO customers
        (customer_code, full_name, email, phone, risk_level)
    VALUES
        ('CUST001', 'Arun Kumar', 'arun@example.com', '9876543210', 'LOW'),
        ('CUST002', 'Priya Shankar', 'priya@example.com', '9876543211', 'MEDIUM'),
        ('CUST003', 'Rahul Raja', 'rahul@example.com', '9876543212', 'HIGH')
    ON CONFLICT (customer_code)
    DO UPDATE SET
        full_name = EXCLUDED.full_name,
        email = EXCLUDED.email,
        phone = EXCLUDED.phone,
        risk_level = EXCLUDED.risk_level;
"""))

        conn.execute(text("""
            INSERT INTO accounts
                (customer_id, account_number, account_type, balance, status)
            SELECT customer_id, 'XXXX4521', 'SAVINGS', 84250.00, 'ACTIVE'
            FROM customers
            WHERE customer_code = 'CUST001'
            ON CONFLICT (account_number) DO NOTHING;
        """))

        conn.execute(text("""
            INSERT INTO accounts
                (customer_id, account_number, account_type, balance, status)
            SELECT customer_id, 'XXXX7812', 'SAVINGS', 125600.00, 'ACTIVE'
            FROM customers
            WHERE customer_code = 'CUST002'
            ON CONFLICT (account_number) DO NOTHING;
        """))

        conn.execute(text("""
            INSERT INTO accounts
                (customer_id, account_number, account_type, balance, status)
            SELECT customer_id, 'XXXX9034', 'CURRENT', 45000.00, 'ACTIVE'
            FROM customers
            WHERE customer_code = 'CUST003'
            ON CONFLICT (account_number) DO NOTHING;
        """))

        conn.execute(text("""
            INSERT INTO transactions
                (account_id, transaction_reference, transaction_type,
                 amount, merchant_name, transaction_status, transaction_location)
            SELECT account_id, 'TXN10001', 'DEBIT', 5000.00,
                   'Amazon', 'SUCCESS', 'Chennai'
            FROM accounts
            WHERE account_number = 'XXXX4521'
            ON CONFLICT (transaction_reference) DO NOTHING;
        """))

        conn.execute(text("""
            INSERT INTO transactions
                (account_id, transaction_reference, transaction_type,
                 amount, merchant_name, transaction_status, transaction_location)
            SELECT account_id, 'TXN10002', 'DEBIT', 5000.00,
                   'Amazon', 'SUCCESS', 'Chennai'
            FROM accounts
            WHERE account_number = 'XXXX4521'
            ON CONFLICT (transaction_reference) DO NOTHING;
        """))

        conn.execute(text("""
            INSERT INTO transactions
                (account_id, transaction_reference, transaction_type,
                 amount, merchant_name, transaction_status, transaction_location)
            SELECT account_id, 'TXN20001', 'DEBIT', 75000.00,
                   'ABC Electronics', 'SUCCESS', 'Mumbai'
            FROM accounts
            WHERE account_number = 'XXXX7812'
            ON CONFLICT (transaction_reference) DO NOTHING;
        """))

        conn.execute(text("""
            INSERT INTO transactions
                (account_id, transaction_reference, transaction_type,
                 amount, merchant_name, transaction_status, transaction_location)
            SELECT account_id, 'TXN30001', 'DEBIT', 1200.00,
                   'Swiggy', 'SUCCESS', 'Chennai'
            FROM accounts
            WHERE account_number = 'XXXX9034'
            ON CONFLICT (transaction_reference) DO NOTHING;
        """))

        conn.execute(text("""
            INSERT INTO support_tickets
                (customer_id, subject, description, category,
                 priority, risk_level, status, ai_confidence)
            SELECT customer_id,
                   'Duplicate transaction',
                   'Customer reported two identical Amazon charges of Rs.5000.',
                   'TRANSACTION_DISPUTE',
                   'HIGH',
                   'MEDIUM',
                   'OPEN',
                   94.00
            FROM customers
            WHERE customer_code = 'CUST001'
            AND NOT EXISTS (
                SELECT 1 FROM support_tickets
                WHERE subject = 'Duplicate transaction'
            );
        """))

    print("Demo banking data inserted successfully.")


if __name__ == "__main__":
    seed_data()