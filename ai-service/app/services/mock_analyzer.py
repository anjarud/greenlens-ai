import time

MOCK_ANALYSIS_DELAY_SECONDS = 5


def analyze_image_mock(original_filename: str | None) -> dict:
    time.sleep(MOCK_ANALYSIS_DELAY_SECONDS)

    return {
        "provider": "mock",
        "original_filename": original_filename,
        "results": [
            {
                "scientific_name": "Monstera deliciosa",
                "common_name": "Swiss cheese plant - Kiki",
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