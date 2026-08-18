from pathlib import Path

import httpx

AI_SERVICE_ANALYZE_URL = "http://127.0.0.1:8001/analyze"


def analyze_image_file(
    image_path: Path,
    filename: str,
    content_type: str,
) -> dict:
    with image_path.open("rb") as image_file:
        files = {
            "file": (
                filename,
                image_file,
                content_type,
            )
        }

        response = httpx.post(
            AI_SERVICE_ANALYZE_URL,
            files=files,
            timeout=30.0,
        )

        response.raise_for_status()
        return response.json()