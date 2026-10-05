import csv
from pathlib import Path
from collections import defaultdict

DATA_FILE = Path("data/demo/transactions.csv")


def load_transactions():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def calculate_total_spending():
    transactions = load_transactions()

    return sum(
        float(row["amount"])
        for row in transactions
        if row["type"] == "expense"
    )


def spending_by_category():
    transactions = load_transactions()
    totals = defaultdict(float)

    for row in transactions:
        if row["type"] == "expense":
            totals[row["category"]] += float(row["amount"])

    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


if __name__ == "__main__":
    total = calculate_total_spending()

    print(f"Total spending: INR {total:,.2f}")
    print("\nSpending by category:")

    for category, amount in spending_by_category().items():
        print(f"{category}: INR {amount:,.2f}")
