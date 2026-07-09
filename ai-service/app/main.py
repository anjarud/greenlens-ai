from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(title="GreenLens AI Service")

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-service"
    }

@app.post("/analyze")
def analyze_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG and WebP images are supported."
        )

    return {
        "provider": "mock",
        "original_filename": file.filename,
        "results": [
            {
                "scientific_name": "Monstera deliciosa",
                "common_name": "Swiss cheese plant",
                "confidence": 0.87
            },
            {
                "scientific_name": "Epipremnum aureum",
                "common_name": "Golden pothos",
                "confidence": 0.09
            },
            {
                "scientific_name": "Philodendron hederaceum",
                "common_name": "Heartleaf philodendron",
                "confidence": 0.04
            }
        ]
    }