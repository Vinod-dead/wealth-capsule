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
    previous_file: str | None = "transactions.csv",
) -> dict:

    plan = plan_request(user_request)

    skill = plan["skill"]

    research_results = []

    # Retrieve relevant persistent memories
    memories = retrieve_memory(user_request)

    # Financial analysis
    if skill in {
        "spending_analysis",
        "monthly_report",
        "budget_review",
    }:
        result = run_analysis(
            skill=skill,
            current_file=current_file,
            previous_file=previous_file or current_file,
        )

    # General financial education
    else:
        result = financial_education(user_request)

    # Tavily research
    if plan.get("needs_research"):
        research_query = plan.get("research_query")

        if research_query:
            research_results = run_research(
                research_query
            )["sources"]

    # Only send privacy-safe financial context to Nemotron
    safe_context = result.get(
        "safe_ai_context",
        {},
    )

    # Generate final answer
    answer = generate_answer(
        safe_context=safe_context,
        user_question=user_request,
        research_results=research_results,
        memories=memories,
    )

    # Validate generated answer
    validation = validate_answer(
        answer=answer,
        safe_context=safe_context,
        research_results=research_results,
    )

    return {
        "plan": plan,
        "result": result,
        "research": research_results,
        "memories": memories,
        "answer": answer,
        "validation": validation,
    }