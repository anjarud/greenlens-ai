import httpx
from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.app.services.ai_service_client import analyze_image_file

from backend.app.services.job_storage import (
    create_job_from_upload,
    load_job_status,
    load_job_result,
    save_job_status,
    save_job_result,
    get_input_file_info
)
router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("", status_code=201)
def create_job(file: UploadFile = File(...)):
    return create_job_from_upload(file)

@router.get("/{job_id}")
def get_job(job_id: str):
    return load_job_status(job_id)

@router.post("/{job_id}/process")
def process_job(job_id: str):
    job_status = load_job_status(job_id)

    input_file_path, stored_filename, content_type = get_input_file_info(
        job_id,
        job_status,
    )

    job_status["status"] = "processing"
    job_status["message"] = "Image analysis is running."
    save_job_status(job_id, job_status)

    try:
        analysis_result = analyze_image_file(
            image_path=input_file_path,
            filename=stored_filename,
            content_type=content_type,
        )

    except httpx.HTTPError as error:
        job_status["status"] = "failed"
        job_status["message"] = f"AI service request failed: {error}"
        save_job_status(job_id, job_status)

        raise HTTPException(
            status_code=502,
            detail="AI service request failed."
        )

    save_job_result(job_id, analysis_result)

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

@router.get("/{job_id}/result")
def get_job_result(job_id: str):
    return load_job_result(job_id)