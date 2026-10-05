import os
from pathlib import Path

from dotenv import load_dotenv
from tavily import TavilyClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

load_dotenv()


def search_public_knowledge(query: str) -> list[dict]:
    """
    Search current public information using Tavily.

    Only public research queries should reach Tavily.
    Private financial transaction data must never be included.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not configured.")

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
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