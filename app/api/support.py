from fastapi import APIRouter
from pydantic import BaseModel
from langgraph.types import Command

from app.agents.banking_workflow import banking_graph


router = APIRouter(
    prefix="/support",
    tags=["AI Banking Support"]
)


class SupportRequest(BaseModel):
    customer_code: str
    message: str
    amount: float = 0
    duplicate_transaction: bool = False
    thread_id: str


class ApprovalRequest(BaseModel):
    thread_id: str
    approved: bool


@router.post("/chat")
def support_chat(request: SupportRequest):

    result = banking_graph.invoke(
        {
            "customer_code": request.customer_code,
            "customer_message": request.message,
            "amount": request.amount,
            "duplicate_transaction": request.duplicate_transaction,

            "customer_360": {},

            "category": "",
            "priority": "",
            "risk_level": "",
            "risk_reasons": [],

            "knowledge": [],
            "response": "",

            "validation": {},
            "human_approved": False,
            "ticket": {}
        },
        config={
            "configurable": {
                "thread_id": request.thread_id
            }
        }
    )

    if "__interrupt__" in result:
        interrupt_info = result["__interrupt__"][0]

        return {
            "status": "HUMAN_APPROVAL_REQUIRED",
            "thread_id": request.thread_id,
            "approval_request": interrupt_info.value
        }

    return {
        "status": "COMPLETED",
        "customer_code": result["customer_code"],
        "category": result["category"],
        "priority": result["priority"],
        "risk_level": result["risk_level"],
        "risk_reasons": result["risk_reasons"],
        "response": result["response"],
        "validation": result["validation"],
        "ticket": result["ticket"]
    }


@router.post("/approve")
def approve_support_case(request: ApprovalRequest):

    result = banking_graph.invoke(
        Command(resume=request.approved),
        config={
            "configurable": {
                "thread_id": request.thread_id
            }
        }
    )

    if "__interrupt__" in result:
        interrupt_info = result["__interrupt__"][0]

        return {
            "status": "HUMAN_APPROVAL_REQUIRED",
            "thread_id": request.thread_id,
            "approval_request": interrupt_info.value
        }

    return {
        "status": "COMPLETED",
        "category": result["category"],
        "priority": result["priority"],
        "risk_level": result["risk_level"],
        "risk_reasons": result["risk_reasons"],
        "response": result["response"],
        "validation": result["validation"],
        "ticket": result["ticket"]
    }