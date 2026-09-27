"""Serve the emotion detector interface and its Watson-backed Flask endpoint."""

import os

from flask import Flask, Response, render_template, request

from EmotionDetection import EmotionServiceError, emotion_detector

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


@app.get("/")
def index():
    """Render the project interface."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Return a readable result, an invalid-input message, or a service error."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text_to_analyze)
    except EmotionServiceError:
        return Response(
            "Emotion service unavailable. Please try again later.",
            status=503,
            mimetype="text/plain",
        )
    if result["dominant_emotion"] is None:
        return Response("Invalid text! Please try again!", mimetype="text/plain")
    message = (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return Response(message, mimetype="text/plain")


@app.after_request
def protect_response(response):
    """Avoid caching submitted text and prevent MIME sniffing."""
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


if __name__ == "__main__":
    # The lab preview proxy needs 0.0.0.0; local runs use loopback by default.
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=5000, debug=False)
