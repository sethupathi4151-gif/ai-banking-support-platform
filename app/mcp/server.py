from mcp.server.mcpserver import MCPServer
from sqlalchemy import text

from app.database.connection import engine


mcp = MCPServer("Banking Support MCP")


@mcp.tool()
def lookup_customer(customer_code: str) -> dict:
    """Look up a customer and their basic account information."""

    with engine.connect() as conn:
        customer = conn.execute(
            text("""
                SELECT customer_id, customer_code, full_name,
                       email, phone, risk_level
                FROM customers
                WHERE customer_code = :customer_code
            """),
            {"customer_code": customer_code}
        ).mappings().first()

        if not customer:
            return {"error": "Customer not found"}

        accounts = conn.execute(
            text("""
                SELECT account_number, account_type,
                       balance, status
                FROM accounts
                WHERE customer_id = :customer_id
                ORDER BY account_id
            """),
            {"customer_id": customer["customer_id"]}
        ).mappings().all()

        return {
            "customer": dict(customer),
            "accounts": [dict(account) for account in accounts]
        }


@mcp.tool()
def create_support_ticket(
    customer_code: str,
    subject: str,
    description: str,
    category: str,
    priority: str,
    risk_level: str
) -> dict:
    """Create a support ticket for a customer."""

    with engine.begin() as conn:
        customer_id = conn.execute(
            text("""
                SELECT customer_id
                FROM customers
                WHERE customer_code = :customer_code
            """),
            {"customer_code": customer_code}
        ).scalar()

        if customer_id is None:
            return {"error": "Customer not found"}

        ticket_id = conn.execute(
            text("""
                INSERT INTO support_tickets
                (
                    customer_id,
                    subject,
                    description,
                    category,
                    priority,
                    risk_level,
                    status
                )
                VALUES
                (
                    :customer_id,
                    :subject,
                    :description,
                    :category,
                    :priority,
                    :risk_level,
                    'OPEN'
                )
                RETURNING ticket_id
            """),
            {
                "customer_id": customer_id,
                "subject": subject,
                "description": description,
                "category": category,
                "priority": priority,
                "risk_level": risk_level
            }
        ).scalar_one()

        return {
            "success": True,
            "ticket_id": ticket_id,
            "status": "OPEN"
        }


@mcp.tool()
def update_ticket_status(ticket_id: int, status: str) -> dict:
    """Update the status of a support ticket."""

    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE support_tickets
                SET status = :status,
                    updated_at = NOW()
                WHERE ticket_id = :ticket_id
            """),
            {
                "ticket_id": ticket_id,
                "status": status
            }
        )

        if result.rowcount == 0:
            return {"error": "Ticket not found"}

        return {
            "success": True,
            "ticket_id": ticket_id,
            "status": status
        }


if __name__ == "__main__":
    mcp.run()