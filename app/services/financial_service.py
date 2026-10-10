from app.finance import (
    load_transactions,
    filter_by_month,
    calculate_total,
    spending_by_category,
    compare_category_changes,
)
from app.privacy.gateway import build_safe_context


def analyze_finances(
    current_file: str,
    previous_file: str | None = None,
    current_year: int | None = None,
    current_month: int | None = None,
    previous_year: int | None = None,
    previous_month: int | None = None,
) -> dict:
    current_transactions = load_transactions(current_file)

    if current_year is not None and current_month is not None:
        current_transactions = filter_by_month(
            current_transactions,
            current_year,
            current_month,
        )

    current_total = calculate_total(current_transactions)
    current_categories = spending_by_category(current_transactions)

    previous_total = None
    previous_categories = {}
    category_changes = {}

    if previous_file:
        previous_transactions = load_transactions(previous_file)

        if previous_year is not None and previous_month is not None:
            previous_transactions = filter_by_month(
                previous_transactions,
                previous_year,
                previous_month,
            )

        previous_total = calculate_total(previous_transactions)
        previous_categories = spending_by_category(previous_transactions)

        category_changes = compare_category_changes(
            previous_categories,
            current_categories,
        )

    safe_context = build_safe_context(
        total_spending=current_total,
        category_totals=current_categories,
        previous_total=previous_total,
        category_changes=category_changes,
    )

    return {
        "analysis": {
            "total_spending": current_total,
            "category_totals": current_categories,
            "previous_total": previous_total,
            "previous_categories": previous_categories,
            "category_changes": category_changes,
        },
        "safe_ai_context": safe_context,
    }
