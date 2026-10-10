import csv
from pathlib import Path
from collections import defaultdict


DATA_DIR = Path("data/demo")


def load_transactions(filename):
    file_path = DATA_DIR / filename

    with file_path.open("r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_by_month(transactions, year: int, month: int):
    """
    Return transactions belonging to a specific year and month.
    """
    return [
        row
        for row in transactions
        if row["date"].startswith(f"{year:04d}-{month:02d}-")
    ]


def calculate_total(transactions):
    return sum(
        float(row["amount"])
        for row in transactions
        if row["type"] == "expense"
    )


def spending_by_category(transactions):
    totals = defaultdict(float)

    for row in transactions:
        if row["type"] == "expense":
            totals[row["category"]] += float(row["amount"])

    return dict(
        sorted(
            totals.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )


def compare_category_changes(previous_categories, current_categories):
    """
    Calculate the actual spending change for each category.

    Positive values mean spending increased.
    Negative values mean spending decreased.
    """

    categories = set(previous_categories) | set(current_categories)

    changes = {
        category: round(
            current_categories.get(category, 0)
            - previous_categories.get(category, 0),
            2,
        )
        for category in categories
    }

    return dict(
        sorted(
            changes.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )


def compare_months(previous_file, current_file):
    previous = load_transactions(previous_file)
    current = load_transactions(current_file)

    previous_total = calculate_total(previous)
    current_total = calculate_total(current)

    change = current_total - previous_total

    if previous_total:
        percentage = (change / previous_total) * 100
    else:
        percentage = 0

    previous_categories = spending_by_category(previous)
    current_categories = spending_by_category(current)

    category_changes = compare_category_changes(
        previous_categories,
        current_categories,
    )

    return {
        "previous_total": previous_total,
        "current_total": current_total,
        "change": change,
        "percentage_change": percentage,
        "previous_categories": previous_categories,
        "current_categories": current_categories,
        "category_changes": category_changes,
    }


if __name__ == "__main__":
    result = compare_months(
        "august_transactions.csv",
        "transactions.csv",
    )

    print(f"August spending: INR {result['previous_total']:,.2f}")
    print(f"Current-period spending: INR {result['current_total']:,.2f}")
    print(f"Change: INR {result['change']:,.2f}")
    print(
        f"Percentage change: "
        f"{result['percentage_change']:.2f}%"
    )

    print("\nCurrent spending by category:")

    for category, amount in result["current_categories"].items():
        print(f"{category}: INR {amount:,.2f}")

    print("\nCategory changes:")

    for category, change in result["category_changes"].items():
        print(f"{category}: INR {change:+,.2f}")