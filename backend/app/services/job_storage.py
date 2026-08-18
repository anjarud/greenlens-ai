import json

from fastapi import HTTPException
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2]
JOBS_DIR = BACKEND_DIR / "data" / "jobs"

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