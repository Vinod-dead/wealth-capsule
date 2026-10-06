from app.services.financial_service import analyze_finances


def spending_analysis(
    current_file: str,
    previous_file: str | None = None,
) -> dict:
    """
    Reusable skill for analyzing spending.

    Financial data is analyzed locally and only
    privacy-safe aggregated context is prepared
    for AI use.
    """

    return analyze_finances(
        current_file=current_file,
        previous_file=previous_file,
        current_year=2026,
        current_month=9,
    )