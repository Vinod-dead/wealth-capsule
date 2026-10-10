import sqlite3
from pathlib import Path


DB_PATH = Path("data/demo/wealth_capsule_memory.db")


STOP_WORDS = {
    "how",
    "what",
    "why",
    "when",
    "where",
    "which",
    "should",
    "could",
    "would",
    "can",
    "does",
    "did",
    "my",
    "me",
    "i",
    "the",
    "a",
    "an",
    "is",
    "are",
    "this",
    "that",
    "for",
    "to",
    "of",
    "and",
}


NORMALIZATION_MAP = {
    "explain": "explain",
    "explains": "explain",
    "explained": "explain",
    "explaining": "explain",
    "explanation": "explain",
    "explanations": "explain",

    "spend": "spend",
    "spending": "spend",
    "spent": "spend",

    "expense": "expense",
    "expenses": "expense",

    "finance": "finance",
    "finances": "finance",
    "financial": "finance",

    "simple": "simple",
    "simplify": "simple",
    "simplified": "simple",
}


def normalize_term(word: str) -> str:
    """
    Normalize related words so memory search can match
    simple variations such as:

    explain -> explanations
    spending -> spent
    financial -> finance
    """
    word = word.strip().lower()

    if not word:
        return ""

    return NORMALIZATION_MAP.get(word, word)


def tokenize(text: str) -> list[str]:
    """
    Convert text into normalized searchable terms.
    """
    if not isinstance(text, str):
        return []

    words = []

    for raw_word in text.lower().split():
        word = (
            raw_word
            .strip(".,!?;:\"'()[]{}")
            .strip()
        )

        if len(word) < 3:
            continue

        if word in STOP_WORDS:
            continue

        normalized = normalize_term(word)

        if normalized:
            words.append(normalized)

    return words


def get_connection():
    """
    Create and return the SQLite connection.
    """
    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DB_PATH)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_type TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    return connection


def save_memory(
    memory_type: str,
    content: str,
) -> None:
    """
    Save one memory.
    """
    if not memory_type or not content:
        return

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO memories (
            memory_type,
            content
        )
        VALUES (?, ?)
        """,
        (
            memory_type.strip(),
            content.strip(),
        ),
    )

    connection.commit()
    connection.close()


def get_memories(
    limit: int = 10,
) -> list[dict]:
    """
    Retrieve the most recent memories.
    """
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            memory_type,
            content,
            created_at
        FROM memories
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    connection.close()

    return [
        {
            "id": row[0],
            "memory_type": row[1],
            "content": row[2],
            "created_at": row[3],
        }
        for row in rows
    ]


def search_memories(
    query: str,
    limit: int = 5,
) -> list[dict]:
    """
    Search memories using normalized word matching.

    Example:

    Query:
        "How should I explain my spending?"

    Memory:
        "User prefers simple financial explanations"

    Matching terms:
        explain
        spend
        finance
    """

    if not isinstance(query, str):
        return []

    if not query.strip():
        return []

    query_terms = set(tokenize(query))

    if not query_terms:
        return []

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            memory_type,
            content,
            created_at
        FROM memories
        """
    ).fetchall()

    connection.close()

    scored_memories = []

    for row in rows:
        memory_id = row[0]
        memory_type = row[1]
        content = row[2]
        created_at = row[3]

        memory_terms = set(tokenize(content))

        matching_terms = (
            query_terms.intersection(memory_terms)
        )

        if not matching_terms:
            continue

        score = len(matching_terms)

        scored_memories.append(
            (
                score,
                memory_id,
                {
                    "id": memory_id,
                    "memory_type": memory_type,
                    "content": content,
                    "created_at": created_at,
                },
            )
        )

    scored_memories.sort(
        key=lambda item: (
            item[0],
            item[1],
        ),
        reverse=True,
    )

    return [
        memory
        for _, _, memory in scored_memories[:limit]
    ]


def delete_memory(
    memory_id: int,
) -> None:
    """
    Delete one specific memory by ID.
    """
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM memories
        WHERE id = ?
        """,
        (memory_id,),
    )

    connection.commit()
    connection.close()