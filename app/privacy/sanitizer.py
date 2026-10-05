from typing import Dict, Any


def sanitize_financial_context(
    total_spending: float,
    category_totals: Dict[str, float],
    previous_total: float | None = None,
) -> Dict[str, Any]:
    """
    Create a minimized financial context for an AI model.

    Raw transaction records are intentionally not included.
    """

    sorted_categories = sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    context = {
        "total_spending": round(total_spending, 2),
        "category_totals": {
            category: round(amount, 2)
            for category, amount in sorted_categories
        },
    }

    if previous_total is not None:
        change = total_spending - previous_total

        percentage_change = (
            (change / previous_total) * 100
            if previous_total != 0
            else 0
        )

        context["previous_total"] = round(previous_total, 2)
        context["change"] = round(change, 2)
        context["percentage_change"] = round(percentage_change, 2)

    return context
