from app.services.financial_service import analyze_finances


def get_financial_summary(
    current_file: str = "transactions.csv",
    previous_file: str | None = "august_transactions.csv",
) -> dict:
    """
    Return an aggregated financial summary.

    This tool reads local transaction data only.
    Raw transaction rows are never returned to external agents.
    """

    result = analyze_finances(
        current_file=current_file,
        previous_file=previous_file,
        current_year=2026,
        current_month=9,
    )

    return {
        "analysis": result["analysis"],
        "safe_ai_context": result["safe_ai_context"],
    }