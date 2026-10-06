from app.agents.planner import plan_request
from app.agents.researcher import run_research
from app.agents.answer_agent import generate_answer
from app.agents.validator import validate_answer
from app.agents.analyst import run_analysis
from app.agents.memory_agent import retrieve_memory
from app.skills.financial_education_skill import financial_education


def handle_request(
    user_request: str,
    current_file: str = "transactions.csv",
    previous_file: str | None = "august_transactions.csv",
) -> dict:
    """
    Route a Wealth Capsule request through local financial
    analysis, public research, and Nemotron.

    Private financial data is analyzed locally.
    Tavily receives only the safe research query created
    by the Planner.
    """

    plan = plan_request(user_request)
    skill = plan["skill"]

    research_results = []
    memories = retrieve_memory(user_request)

    # Pure research request
    if skill == "research":
        research_query = plan.get("research_query")

        if research_query:
            result = run_research(research_query)
        else:
            result = {
                "query": None,
                "sources": [],
                "source_count": 0,
            }

        return {
            "plan": plan,
            "result": result,
        }

    # Run the appropriate private-data skill
    if skill in {
    "spending_analysis",
    "monthly_report",
    "budget_review",
}:
     result = run_analysis(
        skill=skill,
        current_file=current_file,
        previous_file=previous_file,
    )

    else:
     result = financial_education(user_request)
    # ---------------------------------------------------------
    # Tavily research
    # IMPORTANT:
    # Never send the original private user request directly.
    # Use only the Planner's safe public research query.
    # ---------------------------------------------------------
    if plan.get("needs_research"):
        research_query = plan.get("research_query")

        if research_query:
            research_results = run_research(
                research_query
            )["sources"]

    # ---------------------------------------------------------
    # Nemotron
    # Only privacy-safe aggregated financial context is sent.
    # ---------------------------------------------------------
    safe_context = result.get("safe_ai_context")
    if safe_context:
        answer = generate_answer(
            safe_context=safe_context,
            user_question=user_request,
            research_results=research_results,
            memories=memories,
        )

        validation = validate_answer(
            answer=answer,
            safe_context=safe_context,
            research_results=research_results,
        )
    else:
        answer = None
        validation = {
            "valid": False,
            "financial_numbers": {},
            "sources": {},
        }

    return {
        "plan": plan,
        "result": result,
        "research": research_results,
        "memories": memories,
        "answer": answer,
        "validation": validation,
    }
       