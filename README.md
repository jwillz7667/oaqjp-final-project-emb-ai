# Final project

Emotion detection with IBM Watson NLP and Flask for IBM's Developing AI Applications with Python and Flask course. This repository extends the supplied starter.

The application sends text to the Skills Network Watson EmotionPredict service and returns anger, disgust, fear, joy, sadness, and the dominant emotion. Blank or rejected input displays `Invalid text! Please try again!`. Timeouts and service failures produce a controlled error. The interface encodes query parameters and renders responses as plain text.

## Run in the IBM Skills Network Theia lab

The Watson endpoint is provided by the course and is accessible inside its lab. No credentials are embedded in this repository.

```sh
python3 -m pip install -r requirements.txt
python3 test_emotion_detection.py
python3 -m pylint server.py
HOST=0.0.0.0 python3 server.py
```

Use the lab's Launch Application control for port 5000. Local runs bind to `127.0.0.1:5000` by default, but predictions require access to the course service. The Flask development server is for this lab demonstration; a public deployment requires a production WSGI server and operational controls.

## Validation

```sh
python3 -m unittest discover -s tests -v
```

Offline boundary tests explicitly mock network responses. The five tests in `test_emotion_detection.py` call the real Watson service and must run in the lab. Mock results are never presented as live predictions. Live verification and project submission are pending.
