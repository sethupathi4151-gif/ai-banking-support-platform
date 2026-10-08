from typing import Dict


def assess_risk(
    category: str,
    amount: float = 0,
    duplicate_transaction: bool = False,
    customer_risk: str = "LOW"
) -> Dict:

    priority = "LOW"
    risk = customer_risk
    reasons = []

    if duplicate_transaction:
        priority = "HIGH"
        risk = "HIGH"
        reasons.append("Possible duplicate transaction")

    if amount >= 50000:
        priority = "HIGH"
        risk = "HIGH"
        reasons.append("High-value transaction")

    elif amount >= 10000 and priority != "HIGH":
        priority = "MEDIUM"
        risk = "MEDIUM"
        reasons.append("Moderate-value transaction")

    if category.upper() in {
        "TRANSACTION_DISPUTE",
        "FRAUD",
        "UNAUTHORIZED_TRANSACTION"
    }:
        if priority == "LOW":
            priority = "MEDIUM"

        reasons.append("Financial transaction dispute")

    if customer_risk.upper() == "HIGH":
        risk = "HIGH"

        if priority == "LOW":
            priority = "MEDIUM"

        reasons.append("Customer has high risk profile")

    if not reasons:
        reasons.append("No significant risk indicators detected")

    return {
        "priority": priority,
        "risk_level": risk,
        "reasons": reasons
    }