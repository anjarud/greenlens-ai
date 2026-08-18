from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.mock_analyzer import analyze_image_mock

router = APIRouter(tags=["analysis"])

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


@router.post("/analyze")
def analyze_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG and WebP images are supported."
        )

    return analyze_image_mock(file.filename)