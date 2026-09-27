"""Offline boundary tests; mocks do not validate the live Watson model."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection import EmotionServiceError, emotion_detector
from EmotionDetection.emotion_detection import EMOTIONS
from server import app


class TestServiceBoundaries(unittest.TestCase):
    """Check validation and errors using explicitly mocked responses."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_invalid_input(self, post):
        """Reject blank, invalid-type, and excessive input before networking."""
        for value in ("", "   ", None, 7, "x" * 5001):
            with self.subTest(value_type=type(value).__name__):
                self.assertTrue(all(item is None for item in emotion_detector(value).values()))
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_upstream_400(self, post):
        """Return a null dictionary for upstream status 400."""
        post.return_value.status_code = 400
        self.assertEqual(emotion_detector("Unsupported input"),
                         dict.fromkeys((*EMOTIONS, "dominant_emotion")))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_response_contract(self, post):
        """Extract scores, select the maximum, and use a bounded timeout."""
        scores = dict(zip(EMOTIONS, (0.1, 0.2, 0.3, 0.8, 0.4)))
        post.return_value = Mock(status_code=200)
        post.return_value.json.return_value = {"emotionPredictions": [{"emotion": scores}]}
        self.assertEqual(emotion_detector("Example"), {**scores, "dominant_emotion": "joy"})
        self.assertEqual(post.call_args.kwargs["json"], {"raw_document": {"text": "Example"}})
        self.assertEqual(post.call_args.kwargs["timeout"], (5, 30))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_malformed_scores(self, post):
        """Never turn a broken response into a misleading prediction."""
        post.return_value = Mock(status_code=200)
        for payload in ({}, {"emotionPredictions": []},
                        {"emotionPredictions": [{"emotion": dict.fromkeys(EMOTIONS, 2)}]}):
            post.return_value.json.return_value = payload
            with self.assertRaises(EmotionServiceError):
                emotion_detector("Example")

    @patch("EmotionDetection.emotion_detection.requests.post", side_effect=requests.Timeout)
    def test_timeout(self, _post):
        """Translate transport failures into a controlled service exception."""
        with self.assertRaises(EmotionServiceError):
            emotion_detector("Example")


class TestWebInterface(unittest.TestCase):
    """Exercise Flask requests with mocked upstream predictions."""

    def setUp(self):
        """Create an isolated HTTP test client."""
        self.client = app.test_client()

    def test_page_and_blank_input(self):
        """Serve the interface and show the specified blank-input response."""
        self.assertEqual(self.client.get("/").status_code, 200)
        response = self.client.get("/emotionDetector?textToAnalyze=")
        self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    @patch("server.emotion_detector", side_effect=EmotionServiceError("Unavailable"))
    def test_service_failure(self, _detector):
        """Return an explicit 503 without exposing exception internals."""
        response = self.client.get("/emotionDetector?textToAnalyze=Example")
        self.assertEqual(response.status_code, 503)

    @patch("server.emotion_detector")
    def test_output_format(self, detector):
        """Match the required format and keep input out of HTML."""
        detector.return_value = {**dict.fromkeys(EMOTIONS, 0.1), "dominant_emotion": "joy"}
        response = self.client.get("/emotionDetector", query_string={"textToAnalyze": "A & B"})
        detector.assert_called_once_with("A & B")
        self.assertEqual(response.mimetype, "text/plain")
        self.assertIn("The dominant emotion is joy.", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
