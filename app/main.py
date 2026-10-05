from fastapi import FastAPI

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
