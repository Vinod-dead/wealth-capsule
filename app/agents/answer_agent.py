from app.llm.nemotron import ask_nemotron


def generate_answer(
    safe_context: dict,
    user_question: str,
) -> str:
    """
    Generate a user-facing answer using only
    privacy-safe financial context.
    """

    return ask_nemotron(
        safe_context=safe_context,
        user_question=user_question,
    )