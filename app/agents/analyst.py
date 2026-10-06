from app.skills.spending_skill import spending_analysis
from app.skills.monthly_report_skill import generate_monthly_report
from app.skills.budget_review_skill import budget_review


def run_analysis(
    skill: str,
    current_file: str = "transactions.csv",
    previous_file: str | None = "august_transactions.csv",
) -> dict:
    """
    Run private financial analysis.

    This agent operates only on local financial data.
    Raw transactions are not sent to Tavily.
    """

    if skill == "spending_analysis":
        return spending_analysis(
            current_file=current_file,
            previous_file=previous_file,
        )

    if skill == "monthly_report":
        return generate_monthly_report(
            current_file=current_file,
            previous_file=previous_file,
        )

    if skill == "budget_review":
        return budget_review(
            current_file=current_file,
            previous_file=previous_file,
        )

    raise ValueError(
        f"Unsupported analyst skill: {skill}"
    )