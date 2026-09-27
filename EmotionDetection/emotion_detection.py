"""Call the course Watson service and validate its response."""

import math

import requests

SERVICE_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")
MAX_TEXT_LENGTH = 5000


class EmotionServiceError(RuntimeError):
    """Watson could not supply a valid prediction."""


def emotion_detector(text_to_analyze):
    """Return five scores and their dominant emotion; invalid input returns nulls.

    The service is available inside the IBM Skills Network lab. Transport and
    schema failures raise EmotionServiceError rather than fabricating a result.
    """
    invalid_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return invalid_result
    if len(text_to_analyze) > MAX_TEXT_LENGTH:
        return invalid_result
    try:
        response = requests.post(
            SERVICE_URL,
            headers=MODEL_HEADERS,
            json={"raw_document": {"text": text_to_analyze}},
            timeout=(5, 30),
        )
        if response.status_code == 400:
            return invalid_result
        response.raise_for_status()
        values = response.json()["emotionPredictions"][0]["emotion"]
        scores = {}
        for emotion in EMOTIONS:
            value = values[emotion]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("Emotion score must be numeric")
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError("Emotion score must be between zero and one")
            scores[emotion] = value
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as exc:
        raise EmotionServiceError("The emotion service is unavailable.") from exc
    scores["dominant_emotion"] = max(EMOTIONS, key=scores.get)
    return scores
