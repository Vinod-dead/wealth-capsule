
from app.services.financial_service import analyze_finances


def generate_monthly_report(
    current_file: str,
    previous_file: str | None = None,
) -> dict:
    """
    Generate a structured monthly spending report.

    The demo report uses September 2026 as the
    current analysis month.
    """

    result = analyze_finances(
        current_file=current_file,
        previous_file=previous_file,
        current_year=2026,
        current_month=9,
    )

    analysis = result["analysis"]

    return {
        "total_spending": analysis["total_spending"],
        "previous_total": analysis["previous_total"],
        "category_totals": analysis["category_totals"],
        "safe_ai_context": result["safe_ai_context"],
    }
