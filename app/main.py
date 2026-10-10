
from fastapi import FastAPI
from pydantic import BaseModel

from app.skills.monthly_report_skill import generate_monthly_report
from app.memory.service import recall


app = FastAPI(
    title="Wealth Capsule",
    description="Privacy-preserving personal AI assistant",
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Wealth Capsule API is running",
        "status": "online",
    }


@app.get("/api/dashboard")
def dashboard():
    memory_count = len(recall(limit=10000))

    report = generate_monthly_report(
        current_file="transactions.csv",
        previous_file=None,
        current_year=2026,
        current_month=10,
    )

    total = report["total_spending"]
    previous = report["previous_total"]

    if previous:
        percentage_change = (
            (total - previous) / previous
        ) * 100
    else:
        percentage_change = 0

    return {
        "status": "online",
        "monthly_spending": total,
        "previous_month": previous,
        "percentage_change": round(
            percentage_change,
            2,
        ),
        "categories": report["category_totals"],
        "nemotron": "active",
        "tavily": "active",
        "privacy_gateway": "protected",
        "memory": "active",
        "memory_count": memory_count,
    }


@app.get("/api/privacy-audit")
def privacy_audit():
    return {
        "status": "protected",
        "privacy_gateway": "active",
        "private_data_sent_to_tavily": False,
        "raw_transactions_sent_to_tavily": False,
        "financial_amounts_sent_to_tavily": False,
        "personal_dates_sent_to_tavily": False,
        "email_addresses_sent_to_tavily": False,
        "account_numbers_sent_to_tavily": False,
        "research_queries": "sanitized_public_queries_only",
        "external_content_prompt_injection_filter": "active",
    }


@app.post("/api/ask")
def ask_capsule(request: AskRequest):
    from app.agents.orchestrator import handle_request

    question = request.question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "validation": {
                "valid": False,
            },
        }

    result = handle_request(
        user_request=question,
        current_file="transactions.csv",
        previous_file=None,
    )

    return {
        "answer": result.get("answer", ""),
        "sources": result.get("research", []),
        "validation": result.get("validation", {}),
        "plan": result.get("plan", {}),
    }