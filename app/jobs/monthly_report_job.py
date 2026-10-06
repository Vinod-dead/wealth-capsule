from datetime import datetime

from app.skills.monthly_report_skill import generate_monthly_report
from app.memory.database import save_memory


def run_monthly_report_job(
    current_file: str = "transactions.csv",
    previous_file: str = "august_transactions.csv",
):
    """
    Generate the monthly spending report automatically
    and save a summary to persistent SQLite memory.
    """

    report = generate_monthly_report(
        current_file=current_file,
        previous_file=previous_file,
    )

    analysis_date = datetime.now().strftime("%Y-%m-%d")

    memory_content = {
        "generated_at": analysis_date,
        "total_spending": report["total_spending"],
        "previous_total": report["previous_total"],
        "category_totals": report["category_totals"],
    }

    save_memory(
        memory_type="monthly_report",
        content=str(memory_content),
    )

    return report


if __name__ == "__main__":
    report = run_monthly_report_job()

    print("Monthly report generated.")
    print(f"Total spending: INR {report['total_spending']:,.2f}")
    print("Report saved to persistent memory.")