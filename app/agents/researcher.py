from app.skills.research_skill import research_topic


def run_research(query: str) -> dict:
    """
    Research Agent for Wealth Capsule.

    Only public-information queries are sent to Tavily.
    Private financial transaction data must never be passed here.
    """

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Research query must be a non-empty string.")

    return research_topic(query.strip())