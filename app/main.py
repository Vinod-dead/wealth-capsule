from fastapi import FastAPI

from app.memory.service import remember, recall


app = FastAPI(
    title="Wealth Capsule",
    description="Privacy-preserving Personal AI",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "Wealth Capsule",
        "status": "running"
    }


@app.post("/memory")
def add_memory(memory_type: str, content: str):
    remember(memory_type, content)

    return {
        "status": "saved",
        "memory_type": memory_type,
        "content": content,
    }


@app.get("/memory")
def get_memory():
    return {
        "memories": recall()
    }