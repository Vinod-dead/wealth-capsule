from app.memory.database import search_memories


def retrieve_memory(
    user_request: str,
    limit: int = 5,
) -> list[dict]:
    """
    Retrieve memories relevant to the user's request.
    """

    return search_memories(
        query=user_request,
        limit=limit,
    )