from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)


def generate_response(
    customer_message: str,
    category: str,
    priority: str,
    knowledge: list[str],
    customer_360: dict | None = None
) -> str:

    context = "\n\n".join(knowledge)

    customer_context = ""

    if customer_360:
        customer = customer_360.get("customer", {})

        customer_context = f"""
Customer information:
Customer Code: {customer.get("customer_code")}
Customer Name: {customer.get("full_name")}
Customer Risk Level: {customer.get("risk_level")}

Number of Accounts: {len(customer_360.get("accounts", []))}
Number of Recent Transactions: {len(customer_360.get("transactions", []))}
Number of Support Tickets: {len(customer_360.get("support_tickets", []))}
"""

    prompt = f"""
You are an AI banking customer support response agent.

Customer message:
{customer_message}

Detected category:
{category}

Priority:
{priority}

{customer_context}

Relevant banking knowledge:
{context}

Generate a clear, professional and helpful response.

Rules:
- Use the provided banking knowledge.
- Use Customer 360 information only when relevant.
- Do not expose unnecessary sensitive customer information.
- Do not invent bank policies.
- Do not claim that a refund or transaction has been completed.
- If verification or human review is required, clearly mention it.
- Keep the response concise.
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        return response.content[0]["text"].strip()

    return response.content.strip()