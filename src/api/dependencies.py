# src/api/dependencies.py

from src.detection.detector import FaceDetector

from src.recognition.recognizer import (
    FaceRecognizer,
)

from src.recognition.database import (
    FaceDatabase,
)

from src.emotion.classifier import (
    EmotionClassifier,
)

from src.pipeline.frame_processor import (
    FrameProcessor,
)

detector = FaceDetector()

recognizer = FaceRecognizer()

emotion_classifier = EmotionClassifier()

database = FaceDatabase()

processor = FrameProcessor(
    detector=detector,
    recognizer=recognizer,
    emotion_classifier=emotion_classifier,
    database=database,
)
