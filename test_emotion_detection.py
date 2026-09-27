"""Required project examples tested against real Watson responses in the lab."""

import unittest

from EmotionDetection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Verify the five specified examples with the live service."""

    def test_joy(self):
        """Recognize a happy statement."""
        self.assertEqual(emotion_detector("I am glad this happened")["dominant_emotion"], "joy")

    def test_anger(self):
        """Recognize an angry statement."""
        self.assertEqual(
            emotion_detector("I am really mad about this")["dominant_emotion"], "anger"
        )

    def test_disgust(self):
        """Recognize a disgusted statement."""
        self.assertEqual(
            emotion_detector("I feel disgusted just hearing about this")["dominant_emotion"],
            "disgust",
        )

    def test_sadness(self):
        """Recognize a sad statement."""
        self.assertEqual(emotion_detector("I am so sad about this")["dominant_emotion"], "sadness")

    def test_fear(self):
        """Recognize a fearful statement."""
        self.assertEqual(
            emotion_detector("I am really afraid that this will happen")["dominant_emotion"],
            "fear",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
