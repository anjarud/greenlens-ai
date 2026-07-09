import json
import shutil
from pathlib import Path
from uuid import uuid4

import httpx
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(title="GreenLens AI Backend")

BACKEND_DIR = Path(__file__).resolve().parents[1]
JOBS_DIR = BACKEND_DIR / "data" / "jobs"

AI_SERVICE_ANALYZE_URL = "http://127.0.0.1:8001/analyze"

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

CONTENT_TYPES_BY_EXTENSION = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}

def load_job_status(job_id: str) -> dict:
    status_file_path = JOBS_DIR / job_id / "status.json"

    if not status_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    with status_file_path.open("r", encoding="utf-8") as status_file:
        return json.load(status_file)


def save_job_status(job_id: str, job_status: dict) -> None:
    job_dir = JOBS_DIR / job_id
    status_file_path = job_dir / "status.json"

    with status_file_path.open("w", encoding="utf-8") as status_file:
        json.dump(job_status, status_file, indent=2)




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

    file_extension = Path(file.filename or "").suffix.lower()       # e.g. .jpg
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
        "content_type": file.content_type,
    }

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

@app.post("/jobs/{job_id}/process")
def process_job(job_id: str):
    job_status = load_job_status(job_id)

    job_dir = JOBS_DIR / job_id
    input_dir = job_dir / "input"
    result_file_path = job_dir / "result.json"

    stored_filename = job_status.get("stored_filename")

    if not stored_filename:
        raise HTTPException(
            status_code=500,
            detail="Stored filename is missing for this job."
        )

    input_file_path = input_dir / stored_filename

    if not input_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Uploaded image file not found."
        )

    job_status["status"] = "processing"
    job_status["message"] = "Image analysis is running."
    save_job_status(job_id, job_status)

    content_type = job_status.get("content_type")
    if not content_type:
        content_type = CONTENT_TYPES_BY_EXTENSION.get(
            input_file_path.suffix.lower(),
            "application/octet-stream"          # ~unknown MIME type
        )

    try:
        with input_file_path.open("rb") as image_file:
            files = {
                "file": (
                    stored_filename,
                    image_file,
                    content_type,
                )
            }

            response = httpx.post(
                AI_SERVICE_ANALYZE_URL,
                files=files,
                timeout=30.0,
            )

            response.raise_for_status()             # if error -> exception
            analysis_result = response.json()

    except httpx.HTTPError as error:
        job_status["status"] = "failed"
        job_status["message"] = f"AI service request failed: {error}"
        save_job_status(job_id, job_status)

        raise HTTPException(
            status_code=502,
            detail="AI service request failed."
        )

    with result_file_path.open("w", encoding="utf-8") as result_file:
        json.dump(analysis_result, result_file, indent=2)

    job_status["status"] = "finished"
    job_status["message"] = "Image analysis completed successfully."
    job_status["result_file"] = "result.json"
    save_job_status(job_id, job_status)

    return {
        "job_id": job_id,
        "status": "finished",
        "message": "Image analysis completed successfully.",
        "result": analysis_result,
    }


@app.get("/jobs/{job_id}/result")
def get_job_result(job_id: str):
    result_file_path = JOBS_DIR / job_id / "result.json"

    if not result_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Result not found. The job may not have been processed yet."
        )

    with result_file_path.open("r", encoding="utf-8") as result_file:
        return json.load(result_file)