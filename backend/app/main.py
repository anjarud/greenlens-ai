import json
import shutil
from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(title="GreenLens AI Backend")

BACKEND_DIR = Path(__file__).resolve().parents[1]
JOBS_DIR = BACKEND_DIR / "data" / "jobs"

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "backend"
    }

@app.post("/jobs", status_code=201)
def create_job(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image type")

    job_id = str(uuid4())
    job_dir = JOBS_DIR / job_id
    input_dir = job_dir / "input"

    input_dir.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.filename or "").suffix       # e.g. .jpg
    saved_filename = f"original{file_extension}"
    saved_file_path = input_dir / saved_filename

    with saved_file_path.open("wb") as buffer:              # buffer = target_file
        shutil.copyfileobj(file.file, buffer)               # file.file = content of file (source)

    job_status = {
        "job_id": job_id,
        "status": "uploaded",
        "message": "Image uploaded successfully.",
        "original_filename": file.filename,
        "stored_filename": saved_filename,
    }

    status_file_path = job_dir / "status.json"

    status_file_path = job_dir / "status.json"

    with status_file_path.open("w", encoding="utf-8") as status_file:
        json.dump(job_status, status_file, indent=2)                            # intend -> more readable

    return job_status

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status_file_path = JOBS_DIR / job_id / "status.json"

    if not status_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    with status_file_path.open("r", encoding="utf-8") as status_file:
        return json.load(status_file)