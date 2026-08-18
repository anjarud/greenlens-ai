from fastapi import FastAPI

from backend.app.api.jobs import router as jobs_router

app = FastAPI(title="GreenLens AI Backend")

app.include_router(jobs_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "backend"
    }