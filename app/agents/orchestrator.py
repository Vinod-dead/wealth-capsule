from app.agents.planner import plan_request
from app.agents.researcher import run_research
from app.agents.answer_agent import generate_answer

from app.skills.spending_skill import spending_analysis
from app.skills.monthly_report_skill import generate_monthly_report
from app.skills.budget_review_skill import budget_review
from app.skills.financial_education_skill import financial_education


def handle_request(
    user_request: str,
    current_file: str = "transactions.csv",
    previous_file: str | None = "august_transactions.csv",
) -> dict:
    """
    Route a user request to the appropriate Wealth Capsule skill
    and generate a final answer when private financial context
    is available.
    """

    plan = plan_request(user_request)
    skill = plan["skill"]

    if skill == "research":
        result = run_research(user_request)

        return {
            "plan": plan,
            "result": result,
        }

    if skill == "spending_analysis":
        result = spending_analysis(current_file, previous_file)

    elif skill == "monthly_report":
        result = generate_monthly_report(current_file, previous_file)

    elif skill == "budget_review":
        result = budget_review(current_file, previous_file)

    else:
        result = financial_education(user_request)

    safe_context = result.get("safe_ai_context")

    if safe_context:
        answer = generate_answer(
            safe_context=safe_context,
            user_question=user_request,
        )
    else:
        answer = None

    return {
        "plan": plan,
        "result": result,
        "answer": answer,
    }