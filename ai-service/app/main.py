from fastapi import FastAPI

from app.api.analysis import router as analysis_router

app = FastAPI(title="GreenLens AI Service")

app.include_router(analysis_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-service"
    }