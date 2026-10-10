
import app.memory.database as memory_db


def test_memory_persists_and_can_be_retrieved(tmp_path, monkeypatch):
    monkeypatch.setattr(
        memory_db, "DB_PATH", tmp_path / "test_memory.db"
    )

    memory_db.save_memory("test", "Remember this example")
    memories = memory_db.get_memories()

    assert len(memories) == 1
    assert memories[0]["memory_type"] == "test"
    assert memories[0]["content"] == "Remember this example"
