import os

from dotenv import load_dotenv
from openai import OpenAI

from app.services.response_service import clean_model_response


load_dotenv()


client = OpenAI(
    api_key=os.getenv("NEBIUS_API_KEY"),
    base_url="https://api.tokenfactory.nebius.com/v1/",
)


MODEL = "nvidia/Nemotron-3_5-Lightning"


def ask_nemotron(safe_context: dict, user_question: str) -> str:
    """
    Send only privacy-safe financial context to Nemotron.
    """

    prompt = f"""
You are Wealth Capsule, a privacy-preserving personal AI assistant.

Safe financial context:
{safe_context}

User question:
{user_question}

Give a concise answer directly to the user.

Rules:
- Use only the provided financial context.
- Do not invent transactions or personal information.
- Do not provide professional financial advice.
- Return only the final answer.
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
        max_tokens=300,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
    )

    model_text = response.choices[0].message.content

    return clean_model_response(model_text)