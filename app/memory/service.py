from app.memory.database import save_memory, get_memories


def remember(memory_type: str, content: str) -> None:
    """Save a piece of useful user context."""
    save_memory(memory_type, content)


def recall(limit: int = 10) -> list[dict]:
    """Retrieve recent memories."""
    return get_memories(limit)