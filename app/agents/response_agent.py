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
Customer 360 information:
Customer name: {customer.get("full_name", "Unknown")}
Customer risk level: {customer.get("risk_level", "Unknown")}

Accounts:
{customer_360.get("accounts", [])}

Recent transactions:
{customer_360.get("transactions", [])}

Previous support tickets:
{customer_360.get("support_tickets", [])}
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
- Use Customer 360 information only when relevant to the customer's request.
- Do not invent bank policies.
- Do not claim that a refund, transaction, payment, or account action
  has been completed.
- Sensitive banking operations require customer verification.
- Never reveal sensitive account information such as account balance,
  full account number, transaction details, or other private financial
  information unless the provided information explicitly confirms that
  customer verification has been completed.
- If the customer asks for sensitive account information without
  verification, clearly state that customer verification is required
  before providing the information.
- For fraud, unauthorized transactions, suspicious activity, or
  unresolved financial disputes, mention that investigation or human
  review may be required when appropriate.
- If a refund is requested for a duplicate or unauthorized transaction,
  do not confirm the refund. Explain that the transaction must first be
  reviewed and verified.
- Do not expose unnecessary customer information in the response.
- Keep the response concise and customer-friendly.
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        return response.content[0]["text"].strip()

    return response.content.strip()