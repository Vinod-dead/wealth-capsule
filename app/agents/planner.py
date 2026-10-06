def plan_request(user_request: str) -> dict:
    """
    Decide which Wealth Capsule skill should handle a request.
    """

    request = user_request.lower().strip()

    if any(word in request for word in [
        "research",
        "current",
        "latest",
        "how to budget",
        "budgeting methods",
    ]):
        skill = "research"

    elif any(word in request for word in [
        "budget review",
        "review my budget",
        "where am i spending",
    ]):
        skill = "budget_review"

    elif any(word in request for word in [
        "monthly report",
        "monthly spending",
        "report",
    ]):
        skill = "monthly_report"

    elif any(word in request for word in [
        "spending",
        "spent",
        "expense",
        "expenses",
        "increase",
        "decrease",
    ]):
        skill = "spending_analysis"

    else:
        skill = "financial_education"

    return {
        "request": user_request,
        "skill": skill,
    }