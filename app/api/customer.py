from fastapi import APIRouter, HTTPException

from app.database.customer_service import fetch_customer_360


router = APIRouter(
    prefix="/customers",
    tags=["Customer 360"]
)


@router.get("/{customer_code}")
def get_customer_360(customer_code: str):

    customer_360 = fetch_customer_360(customer_code)

    if not customer_360:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer_360