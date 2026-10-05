import sqlite3
from pathlib import Path


DB_PATH = Path("data/demo/wealth_capsule_memory.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

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


def save_memory(memory_type: str, content: str) -> None:
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO memories (memory_type, content)
        VALUES (?, ?)
        """,
        (memory_type, content),
    )

    connection.commit()
    connection.close()


def get_memories(limit: int = 10) -> list[dict]:
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, memory_type, content, created_at
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