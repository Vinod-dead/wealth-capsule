from app.tools.tavily_tool import search_public_knowledge


def research_topic(query: str) -> dict:
    """
    Reusable research skill for current public information.

    Only the public research query is sent to Tavily.
    Private financial data is never included.
    """

    results = search_public_knowledge(query)

    return {
        "query": query,
        "sources": results,
        "source_count": len(results),
    }