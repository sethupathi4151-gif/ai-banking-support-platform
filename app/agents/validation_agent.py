from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)


def validate_response(
    customer_message: str,
    response: str,
    knowledge: list[str]
) -> dict:

    context = "\n\n".join(knowledge)

    prompt = f"""
You are a banking response quality validation agent.

Customer message:
{customer_message}

Generated response:
{response}

Banking knowledge:
{context}

Check whether the generated response is safe, relevant, accurate,
and supported by the provided knowledge.

Return ONLY this format:

VALID=<YES or NO>
REASON=<short reason>
"""

    result = llm.invoke(prompt)

    if isinstance(result.content, list):
        text = result.content[0]["text"].strip()
    else:
        text = result.content.strip()

    valid = "NO"
    reason = "Validation failed"

    for line in text.splitlines():
        if line.startswith("VALID="):
            valid = line.split("=", 1)[1].strip()

        elif line.startswith("REASON="):
            reason = line.split("=", 1)[1].strip()

    return {
        "valid": valid,
        "reason": reason
    }