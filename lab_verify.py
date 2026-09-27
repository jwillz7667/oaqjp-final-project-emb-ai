"""Run genuine lab checks and retain the exact output for project submission."""

import json
from pathlib import Path
import subprocess
import sys

from EmotionDetection import emotion_detector
from stages.emotion_detection_raw import emotion_detector as raw_detector


def record(filename, output):
    """Save evidence without replacing it with expected or simulated results."""
    evidence = Path(__file__).parent / "evidence"
    evidence.mkdir(exist_ok=True)
    (evidence / filename).write_text(output, encoding="utf-8")
    print(output, flush=True)


def command_check(filename, arguments):
    """Capture a verification command and stop on any failing check."""
    result = subprocess.run(arguments, text=True, capture_output=True, check=False)
    output = "$ " + " ".join(arguments) + "\n" + result.stdout + result.stderr
    record(filename, output)
    result.check_returncode()


def main():
    """Collect raw, formatted, package, model-test, and lint evidence in the lab."""
    raw = raw_detector("I love this new technology.")
    record("2b_application_creation.txt",
           '>>> from stages.emotion_detection_raw import emotion_detector\n'
           '>>> emotion_detector("I love this new technology.")\n' + raw + "\n")
    for filename, statement, expected in (
        ("3b_formatted_output_test.txt", "I am so happy I am doing this", "joy"),
        ("4b_packaging_test.txt", "I hate working long hours", "anger"),
    ):
        result = emotion_detector(statement)
        record(filename, '>>> from EmotionDetection import emotion_detector\n'
               f">>> emotion_detector({statement!r})\n"
               + json.dumps(result, indent=2) + "\n")
        if result["dominant_emotion"] != expected:
            raise RuntimeError(f"Unexpected live prediction for {statement!r}")
    command_check("5b_unit_testing_result.txt", [sys.executable, "test_emotion_detection.py"])
    command_check("offline_boundary_tests.txt",
                  [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    command_check("8b_static_code_analysis.txt", [sys.executable, "-m", "pylint", "server.py"])
    print("All live checks passed. Evidence is saved in evidence/.", flush=True)


if __name__ == "__main__":
    main()
