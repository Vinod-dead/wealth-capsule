from app.privacy.query_rewriter import build_public_research_query


def plan_request(user_request: str) -> dict:
    """
    Decide which Wealth Capsule skill should handle a request
    and whether current public research is needed.
    """

    request = user_request.lower().strip()

    financial_terms = [
        "spending",
        "spent",
        "expense",
        "expenses",
        "increase",
        "decrease",
    ]

    research_terms = [
        "research",
        "current",
        "latest",
        "today",
        "recent",
        "how to budget",
        "budgeting methods",
        "budgeting strategies",
        "strategies",
    ]

    needs_financial_analysis = any(
        word in request for word in financial_terms
    )

    needs_research = any(
        word in request for word in research_terms
    )

    if (
        "monthly report" in request
        or "monthly spending report" in request
    ):
        skill = "monthly_report"

    elif (
        "budget review" in request
        or "review my budget" in request
    ):
        skill = "budget_review"

    elif needs_financial_analysis:
        skill = "spending_analysis"

    elif needs_research:
        skill = "research"

    else:
        skill = "financial_education"

    research_query = None

    if needs_research:
        research_query = build_public_research_query(
            user_request
        )

    return {
        "request": user_request,
        "skill": skill,
        "needs_research": needs_research,
        "research_query": research_query,
    }