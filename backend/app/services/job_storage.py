import json
import json
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile


BACKEND_DIR = Path(__file__).resolve().parents[2]
JOBS_DIR = BACKEND_DIR / "data" / "jobs"

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


def load_job_result(job_id: str) -> dict:
    result_file_path = JOBS_DIR / job_id / "result.json"

    if not result_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Result not found. The job may not have been processed yet."
        )

    with result_file_path.open("r", encoding="utf-8") as result_file:
        return json.load(result_file)

def save_job_result(job_id: str, result: dict) -> None:
    result_file_path = JOBS_DIR / job_id / "result.json"

    with result_file_path.open("w", encoding="utf-8") as result_file:
        json.dump(result, result_file, indent=2)


def create_job_from_upload(file: UploadFile) -> dict:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image type"
        )

    job_id = str(uuid4())
    job_dir = JOBS_DIR / job_id
    input_dir = job_dir / "input"

    input_dir.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.filename or "").suffix.lower()
    saved_filename = f"original{file_extension}"
    saved_file_path = input_dir / saved_filename

    with saved_file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job_status = {
        "job_id": job_id,
        "status": "uploaded",
        "message": "Image uploaded successfully.",
        "original_filename": file.filename,
        "stored_filename": saved_filename,
        "content_type": file.content_type,
    }

    save_job_status(job_id, job_status)

    return job_status

def get_input_file_info(job_id: str, job_status: dict) -> tuple[Path, str, str]:
    stored_filename = job_status.get("stored_filename")

    if not stored_filename:
        raise HTTPException(
            status_code=500,
            detail="Stored filename is missing for this job."
        )

    input_file_path = JOBS_DIR / job_id / "input" / stored_filename

    if not input_file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Uploaded image file not found."
        )

    content_type = job_status.get("content_type")

    if not content_type:
        content_type = CONTENT_TYPES_BY_EXTENSION.get(
            input_file_path.suffix.lower(),
            "application/octet-stream"
        )

    return input_file_path, stored_filename, content_type


def save_job_status(job_id: str, job_status: dict) -> None:
    job_dir = JOBS_DIR / job_id
    status_file_path = job_dir / "status.json"

    with status_file_path.open("w", encoding="utf-8") as status_file:
        json.dump(job_status, status_file, indent=2)