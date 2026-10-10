import os
from pathlib import Path

from dotenv import load_dotenv
from tavily import TavilyClient

from app.privacy.tavily_policy import validate_tavily_query


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def is_relevant_source(result: dict) -> bool:
    """
    Keep sources specifically relevant to personal budgeting.
    """

    title = (result.get("title") or "").lower()
    content = (result.get("content") or "").lower()

    text = f"{title} {content}"

    # Reject obvious non-personal-finance topics.
    blocked_terms = [
        "government budget",
        "federal budget",
        "presidential budget",
        "trump budget",
        "congressional budget",
        "defense spending",
        "government spending",
        "state budget",
        "national budget",
        "political spending",
        "election",
    ]

    if any(term in text for term in blocked_terms):
        return False

    # Require personal-finance relevance.
    relevant_terms = [
        "personal finance",
        "personal budgeting",
        "personal budget",
        "household budget",
        "household expenses",
        "reduce personal expenses",
        "reduce expenses",
        "reduce spending",
        "cut expenses",
        "cut spending",
        "saving money",
        "save money",
        "budgeting",
        "discretionary spending",
        "monthly expenses",
        "manage expenses",
    ]

    return any(
        term in text
        for term in relevant_terms
    )



def search_public_knowledge(query: str) -> list[dict]:
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
    max_results=8,
    include_domains=[
        "truist.com",
        "debt.org",
        "ncoa.org",
        "bankschaumburg.com",
        "aspireapp.com",
        "bankerslife.com",
        "wintrust.com",
    ],
)

    sources = []

    seen_urls = set()

    for result in response.get("results", []):
        title = result.get("title")
        url = result.get("url")
        content = result.get("content")

        if not title or not url:
            continue

        # Remove duplicate URLs.
        if url in seen_urls:
            continue

        # Remove irrelevant search results.
        if not is_relevant_source(result):
            continue

        seen_urls.add(url)

        sources.append(
            {
                "title": title,
                "url": url,
                "content": content,
            }
        )

        # Keep the final research set focused.
        if len(sources) >= 5:
            break

    return sources
