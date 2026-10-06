import os
from pathlib import Path

from dotenv import load_dotenv
from tavily import TavilyClient

from app.privacy.tavily_policy import validate_tavily_query


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def search_public_knowledge(query: str) -> list[dict]:
    """
    Search current public information using Tavily.

    A deterministic privacy policy runs before the external
    Tavily request. Sensitive queries are blocked.
    """

    policy = validate_tavily_query(query)

    if not policy["allowed"]:
        raise ValueError(
            f"Tavily query blocked by privacy policy: "
            f"{policy['reason']}"
        )

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise RuntimeError(
            "TAVILY_API_KEY is not configured."
        )

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query.strip(),
        search_depth="basic",
        max_results=5,
    )

    return [
        {
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content"),
        }
        for result in response.get("results", [])
    ]