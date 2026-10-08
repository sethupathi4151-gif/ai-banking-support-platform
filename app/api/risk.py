from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.risk_agent import assess_risk
from app.database.connection import engine
from sqlalchemy import text


router = APIRouter(prefix="/risk", tags=["Risk Detection"])


class RiskRequest(BaseModel):
    customer_code: str
    category: str
    amount: float = 0
    duplicate_transaction: bool = False


@router.post("/assess")
def assess_customer_risk(request: RiskRequest):

    with engine.connect() as conn:
        customer = conn.execute(
            text("""
                SELECT risk_level
                FROM customers
                WHERE customer_code = :customer_code
            """),
            {"customer_code": request.customer_code}
        ).scalar()

    if customer is None:
        return {
            "error": "Customer not found"
        }

    result = assess_risk(
        category=request.category,
        amount=request.amount,
        duplicate_transaction=request.duplicate_transaction,
        customer_risk=customer
    )

    return {
        "customer_code": request.customer_code,
        **result
    }