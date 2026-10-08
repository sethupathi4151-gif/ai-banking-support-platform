from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

from app.agents.router_agent import router_graph
from app.agents.risk_agent import assess_risk
from app.agents.rag_agent import search_knowledge
from app.agents.response_agent import generate_response
from app.agents.validation_agent import validate_response
from app.database.customer_service import fetch_customer_360
from app.mcp.server import create_support_ticket


class BankingState(TypedDict):
    customer_code: str
    customer_message: str
    amount: float
    duplicate_transaction: bool

    customer_360: dict

    category: str
    priority: str
    risk_level: str
    risk_reasons: list[str]

    knowledge: list[str]
    response: str

    validation: dict
    human_approved: bool
    ticket: dict


def customer_360_node(state: BankingState):
    customer_360 = fetch_customer_360(
        state["customer_code"]
    )

    if not customer_360:
        raise ValueError(
            f"Customer not found: {state['customer_code']}"
        )

    return {
        "customer_360": customer_360
    }


def router_node(state: BankingState):
    result = router_graph.invoke(
        {
            "customer_message": state["customer_message"],
            "category": "",
            "priority": ""
        }
    )

    return {
        "category": result["category"],
        "priority": result["priority"]
    }


def risk_node(state: BankingState):
    customer_risk = (
        state["customer_360"]
        .get("customer", {})
        .get("risk_level", "LOW")
    )

    result = assess_risk(
        category=state["category"],
        amount=state["amount"],
        duplicate_transaction=state["duplicate_transaction"],
        customer_risk=customer_risk
    )

    return {
        "priority": result["priority"],
        "risk_level": result["risk_level"],
        "risk_reasons": result["reasons"]
    }


def rag_node(state: BankingState):
    knowledge = search_knowledge(
        state["customer_message"]
    )

    return {
        "knowledge": knowledge
    }


def response_node(state: BankingState):
    response = generate_response(
        customer_message=state["customer_message"],
        category=state["category"],
        priority=state["priority"],
        knowledge=state["knowledge"],
        customer_360=state["customer_360"]
    )

    return {
        "response": response
    }


def validation_node(state: BankingState):
    validation = validate_response(
        customer_message=state["customer_message"],
        response=state["response"],
        knowledge=state["knowledge"]
    )

    return {
        "validation": validation
    }


def human_review_node(state: BankingState):
    decision = interrupt(
        {
            "message": (
                "Human approval required for this "
                "high-risk banking case."
            ),
            "customer_code": state["customer_code"],
            "category": state["category"],
            "priority": state["priority"],
            "risk_level": state["risk_level"],
            "customer_message": state["customer_message"],
            "generated_response": state["response"]
        }
    )

    return {
        "human_approved": bool(decision)
    }


def action_node(state: BankingState):
    is_high_risk = (
        state["priority"] == "HIGH"
        or state["risk_level"] == "HIGH"
    )

    # High-risk cases require explicit human approval.
    if is_high_risk:
        if state.get("human_approved") is not True:
            return {
                "ticket": {
                    "success": False,
                    "message": "Human approval required"
                }
            }

    validation = state["validation"]

    if (
        validation.get("valid") == "YES"
        and is_high_risk
    ):
        ticket = create_support_ticket(
            customer_code=state["customer_code"],
            subject=state["category"],
            description=state["customer_message"],
            category=state["category"],
            priority=state["priority"],
            risk_level=state["risk_level"]
        )
    else:
        ticket = {
            "success": False,
            "message": "No ticket creation required"
        }

    return {
        "ticket": ticket
    }


def route_after_validation(state: BankingState):
    if (
        state["priority"] == "HIGH"
        or state["risk_level"] == "HIGH"
    ):
        return "human_review"

    return "action"


graph_builder = StateGraph(BankingState)

graph_builder.add_node(
    "customer_360",
    customer_360_node
)

graph_builder.add_node(
    "router",
    router_node
)

graph_builder.add_node(
    "risk",
    risk_node
)

graph_builder.add_node(
    "rag",
    rag_node
)

graph_builder.add_node(
    "response",
    response_node
)

graph_builder.add_node(
    "validation",
    validation_node
)

graph_builder.add_node(
    "human_review",
    human_review_node
)

graph_builder.add_node(
    "action",
    action_node
)


graph_builder.add_edge(
    START,
    "customer_360"
)

graph_builder.add_edge(
    "customer_360",
    "router"
)

graph_builder.add_edge(
    "router",
    "risk"
)

graph_builder.add_edge(
    "risk",
    "rag"
)

graph_builder.add_edge(
    "rag",
    "response"
)

graph_builder.add_edge(
    "response",
    "validation"
)


graph_builder.add_conditional_edges(
    "validation",
    route_after_validation,
    {
        "human_review": "human_review",
        "action": "action"
    }
)


graph_builder.add_edge(
    "human_review",
    "action"
)

graph_builder.add_edge(
    "action",
    END
)


memory = MemorySaver()

banking_graph = graph_builder.compile(
    checkpointer=memory
)