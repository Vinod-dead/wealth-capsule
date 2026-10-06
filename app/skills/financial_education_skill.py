from app.tools.tavily_tool import search_public_knowledge


def financial_education(query: str) -> list[dict]:
    """
    Research current public financial education information.

    Only the user's public-information question is sent to Tavily.
    Private financial transaction data is never included.
    """

    return search_public_knowledge(query)