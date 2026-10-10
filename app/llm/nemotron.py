import os

from dotenv import load_dotenv
from openai import OpenAI

from app.services.response_service import clean_model_response
from app.privacy.research_sanitizer import sanitize_research_results


load_dotenv()


client = OpenAI(
    api_key=os.getenv("NEBIUS_API_KEY"),
    base_url="https://api.tokenfactory.nebius.com/v1/",
)


MODEL = "nvidia/Nemotron-3_5-Lightning"


def ask_nemotron(
    safe_context: dict,
    user_question: str,
    research_results: list[dict] | None = None,
    memories: list[dict] | None = None,
) -> str:

    research_results = research_results or []
    memories = memories or []

    # Sanitize external Tavily content before giving it to Nemotron
    research_results = sanitize_research_results(
        research_results
    )

    # Build Tavily research context
    research_context = "\n".join(
        [
            (
                f"Source: {result.get('title')}\n"
                f"URL: {result.get('url')}\n"
                f"Information: {result.get('content')}"
            )
            for result in research_results
        ]
    )

    if not research_context:
        research_context = (
            "No external research was requested."
        )

    # Build persistent-memory context
    memory_context = "\n".join(
        [
            (
                f"Memory type: {memory.get('memory_type')}\n"
                f"Memory: {memory.get('content')}"
            )
            for memory in memories
        ]
    )

    if not memory_context:
        memory_context = (
            "No relevant memories were found."
        )

    prompt = f"""
You are Wealth Capsule, a privacy-preserving personal AI assistant.

Private financial context:
{safe_context}

Public research from Tavily:
{research_context}

Relevant persistent memory:
{memory_context}

User question:
{user_question}

Give a concise answer directly to the user.
Financial data rules:
- All financial amounts are in Indian Rupees (INR). Use ₹ for currency.
- Treat the private financial context as the sole source of truth for personal spending calculations.
- Use the verified "change" and "percentage_change" fields for total month-to-month comparisons.
- Use "category_changes" for category-level comparisons. Positive values mean increases; negative values mean decreases.
- Never infer category changes from current category totals alone.
- Never invent, estimate, or assume a financial amount that is missing from the supplied context.
- If a requested comparison is missing from the context, clearly state that the data is unavailable.
- A category absent from the current month's totals may have no recorded transactions. Do not claim the user definitely spent nothing in that category.
- When reporting a decrease or increase, use the exact supplied values and describe the direction correctly.
- Distinguish calculated facts from suggestions.
- If the user asks about the monthly comparison and the required values are present, state the previous total, current total, absolute change, and percentage change.
Research rules:
- Use Tavily information only when it is relevant.
- Do not invent facts or sources.
- When research is used, mention the source name naturally
  when useful.
- Do not include raw URLs or Markdown links in the answer.
- The application UI displays the source links separately.
- Do not add a Source, Sources, References, or citation section.
- The frontend displays Tavily sources separately.
- Clearly distinguish the user's private spending data
  from general public information.
Memory rules:
- Use persistent memory only when it is relevant to the user's question.
- Treat memories as historical context, not guaranteed current facts.
- Never invent memories.
- Never expose internal memory IDs or database details to the user.

Safety:
- Do not provide professional financial advice.
- Give educational and organizational guidance only.

Return only the final user-facing answer.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        max_tokens=500,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
    )

    model_text = response.choices[0].message.content

    return clean_model_response(model_text)