from datetime import date

from app.services.financial_service import analyze_finances


def generate_monthly_report(
    current_file: str,
    previous_file: str | None = None,
    current_year: int | None = None,
    current_month: int | None = None,
) -> dict:
    """
    Generate a monthly spending report comparing the selected
    month with the immediately preceding calendar month.
    """

    today = date.today()

    year = current_year if current_year is not None else today.year
    month = current_month if current_month is not None else today.month

    if month == 1:
        previous_year = year - 1
        previous_month = 12
    else:
        previous_year = year
        previous_month = month - 1

    result = analyze_finances(
        current_file=current_file,
        previous_file=previous_file or current_file,
        current_year=year,
        current_month=month,
        previous_year=previous_year,
        previous_month=previous_month,
    )

    analysis = result["analysis"]

    return {
        "total_spending": analysis["total_spending"],
        "previous_total": analysis["previous_total"],
        "category_totals": analysis["category_totals"],
        "previous_categories": analysis["previous_categories"],
        "category_changes": analysis["category_changes"],
        "safe_ai_context": result["safe_ai_context"],
    }
