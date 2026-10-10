def build_public_research_query(user_request: str) -> str:
    """
    Convert a user request into a generic public-information
    query suitable for Tavily.

    Private financial details must never be included.
    """

    request = user_request.lower()

    if any(
        phrase in request
        for phrase in [
            "reduce my spending",
            "reduce spending",
            "cut my spending",
            "spending increase",
            "spent more",
            "budget",
            "budgeting",
        ]
    ):
        return "current strategies for reducing discretionary spending"

    if any(
        phrase in request
        for phrase in [
            "saving",
            "save money",
        ]
    ):
        return "current personal saving strategies and budgeting methods"

    if any(
        phrase in request
        for phrase in [
            "expense",
            "expenses",
            "spending",
    ]):
        return "current strategies for managing monthly expenses"

    return "current personal finance budgeting strategies"