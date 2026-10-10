from app.llm.nemotron import ask_nemotron


def generate_answer(
    safe_context: dict,
    user_question: str,
    research_results: list[dict] | None = None,
    memories: list[dict] | None = None,
) -> str:
    return ask_nemotron(
        safe_context=safe_context,
        user_question=user_question,
        research_results=research_results,
        memories=memories,
    )