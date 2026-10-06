
from app.services.financial_service import analyze_finances


def budget_review(
    current_file: str,
    previous_file: str | None = None,
) -> dict:
    """
    Review September 2026 spending patterns and highlight
    categories that may need attention.

    This is educational guidance, not professional
    financial advice.
    """

    result = analyze_finances(
        current_file=current_file,
        previous_file=previous_file,
        current_year=2026,
        current_month=9,
    )

    analysis = result["analysis"]
    categories = analysis["category_totals"]
    total = analysis["total_spending"]

    category_percentages = {
        category: round((amount / total) * 100, 2)
        for category, amount in categories.items()
    }

    largest_categories = sorted(
        category_percentages.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:3]

    return {
        "total_spending": total,
        "category_percentages": category_percentages,
        "largest_categories": largest_categories,
        "safe_ai_context": result["safe_ai_context"],
        "note": "For educational budgeting guidance only.",
    }
