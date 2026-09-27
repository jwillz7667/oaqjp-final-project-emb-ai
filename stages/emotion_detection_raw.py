"""Task 2 version: return the actual Watson response body before formatting."""

import requests

from EmotionDetection.emotion_detection import MODEL_HEADERS, SERVICE_URL


def emotion_detector(text_to_analyze):
    """Request an emotion prediction and return its original response text."""
    response = requests.post(
        SERVICE_URL,
        headers=MODEL_HEADERS,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=(5, 30),
    )
    response.raise_for_status()
    return response.text
