
from app.privacy.query_rewriter import build_public_research_query


def plan_request(user_request: str) -> dict:
    """Choose a skill and decide whether public research is needed."""

    request = user_request.lower().strip()

    financial_terms = [
        "spending", "spent", "expense", "expenses",
        "increase", "decrease", "transaction", "transactions",
    ]

    research_terms = [
        "research", "current", "latest", "today", "recent",
        "how to budget", "budgeting methods",
        "budgeting strategies", "strategies",
    ]

    needs_financial_analysis = any(
        term in request for term in financial_terms
    )
    explicitly_requests_research = any(
        term in request for term in research_terms
    )

    if "monthly spending report" in request or "monthly report" in request:
        skill = "monthly_report"
    elif "budget review" in request or "review my budget" in request:
        skill = "budget_review"
    elif needs_financial_analysis:
        skill = "spending_analysis"
    elif explicitly_requests_research:
        skill = "research"
    else:
        skill = "financial_education"

    # Local financial questions should not automatically trigger web research.
    needs_research = (
        explicitly_requests_research
        and not needs_financial_analysis
    )

    research_query = (
        build_public_research_query(user_request)
        if needs_research
        else None
    )

    return {
        "request": user_request,
        "skill": skill,
        "needs_research": needs_research,
        "research_query": research_query,
    }
