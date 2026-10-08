from dotenv import load_dotenv

load_dotenv()

from typing import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END


class RouterState(TypedDict):
    customer_message: str
    category: str
    priority: str


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)


def classify_request(state: RouterState):
    prompt = f"""
You are a banking customer support classification agent.

Classify the following customer message.

Customer message:
{state["customer_message"]}

Choose exactly one category:

TRANSACTION_DISPUTE
FRAUD
ACCOUNT
CARD
LOAN
PAYMENT
GENERAL

Choose priority:

LOW
MEDIUM
HIGH

Return ONLY this format:

CATEGORY=<category>
PRIORITY=<priority>
"""

    response = llm.invoke(prompt)
    result = response.content[0]["text"].strip()

    category = "GENERAL"
    priority = "LOW"

    for line in result.splitlines():
        if line.startswith("CATEGORY="):
            category = line.split("=", 1)[1].strip()

        elif line.startswith("PRIORITY="):
            priority = line.split("=", 1)[1].strip()

    return {
        "category": category,
        "priority": priority
    }


graph_builder = StateGraph(RouterState)

graph_builder.add_node("classify_request", classify_request)

graph_builder.add_edge(START, "classify_request")
graph_builder.add_edge("classify_request", END)

router_graph = graph_builder.compile()