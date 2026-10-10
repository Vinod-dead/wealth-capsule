from datetime import date

from app.skills.monthly_report_skill import generate_monthly_report
from app.memory.database import get_memories, save_memory


def run_monthly_report_job(
    current_file: str = "transactions.csv",
    previous_file: str = "august_transactions.csv",
    current_year: int | None = None,
    current_month: int | None = None,
):
    """
    Generate the monthly spending report automatically.

    The same year/month report is saved only once.
    """

    today = date.today()

    year = current_year if current_year is not None else today.year
    month = current_month if current_month is not None else today.month

    report = generate_monthly_report(
        current_file=current_file,
        previous_file=previous_file,
        current_year=year,
        current_month=month,
    )

    report_key = f"{year:04d}-{month:02d}"

    existing_memories = get_memories(limit=100)

    already_saved = any(
        memory["memory_type"] == "monthly_report"
        and f'"report_month": "{report_key}"' in memory["content"]
        for memory in existing_memories
    )

    if not already_saved:
        memory_content = {
            "report_month": report_key,
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
    print("Report memory checked.")
