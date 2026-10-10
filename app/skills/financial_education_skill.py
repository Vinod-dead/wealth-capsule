from app.privacy.query_rewriter import build_public_research_query
from app.tools.tavily_tool import search_public_knowledge


def financial_education(query: str) -> dict:
    """
    Research current public financial education information.

    Only a privacy-safe public research query is sent to Tavily.
    Private financial transaction data is never included.
    """

    research_query = build_public_research_query(query)

    sources = search_public_knowledge(research_query)

    return {
        "safe_ai_context": {},
        "research_query": research_query,
        "sources": sources,
    }
