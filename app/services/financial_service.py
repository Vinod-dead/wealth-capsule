from app.finance import (
    load_transactions,
    calculate_total,
    spending_by_category,
)
from app.privacy.gateway import build_safe_context


def analyze_finances(
    current_file: str,
    previous_file: str | None = None,
) -> dict:
    """
    Analyze private financial data locally and create
    a privacy-safe context for the AI model.
    """

    current_transactions = load_transactions(current_file)

    current_total = calculate_total(current_transactions)
    current_categories = spending_by_category(current_transactions)

    previous_total = None

    if previous_file:
        previous_transactions = load_transactions(previous_file)
        previous_total = calculate_total(previous_transactions)

    safe_context = build_safe_context(
        total_spending=current_total,
        category_totals=current_categories,
        previous_total=previous_total,
    )

    return {
        "analysis": {
            "total_spending": current_total,
            "category_totals": current_categories,
            "previous_total": previous_total,
        },
        "safe_ai_context": safe_context,
    }