from app.skills.research_skill import research_topic


def run_research(query: str) -> dict:
    """
    Research Agent for Wealth Capsule.

    Only public-information queries are sent to Tavily.
    Private financial transaction data must never be passed here.
    """

    return research_topic(query)