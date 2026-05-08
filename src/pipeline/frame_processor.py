# src/pipeline/frame_processor.py

import cv2

from src.pipeline.filters import (
    keep_largest_face,
    is_valid_detection,
    is_valid_face_size,
)

from src.config.settings import (
    SCALE,
    DETECTION_INTERVAL,
    RECOGNITION_INTERVAL,
    EMOTION_INTERVAL,
    MIN_CONFIDENCE,
    MIN_FACE_SIZE,
)

from collections import deque, Counter


class FrameProcessor:

    def __init__(
        self,
        detector,
        recognizer,
        database,
        emotion_classifier,
    ):

        self.detector = detector
        self.recognizer = recognizer
        self.known_faces = database.load_all_embeddings()
        self.emotion_classifier = emotion_classifier

        self.last_recognition = {
            "name": "Unknown",
            "score": 0,
        }

        self.last_emotion = {"emotion": "neutral", "score": 0}

        self.faces = []

        self.emotion_history = deque(maxlen=3)

    def get_stable_emotion(self, emotion):

        self.emotion_history.append(emotion)

        emotion_counts = Counter(self.emotion_history)

        stable_emotion = emotion_counts.most_common(1)[0][0]

        return stable_emotion

    def process(
        self,
        frame,
        frame_count,
    ):

        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=SCALE,
            fy=SCALE,
        )

        if frame_count % DETECTION_INTERVAL != 0:
            return self.faces

        detections = self.detector.detect(small_frame)

        detections = keep_largest_face(detections)

        self.faces = []

        h_frame, w_frame = frame.shape[:2]

        for det in detections:

            if not is_valid_detection(
                det,
                MIN_CONFIDENCE,
            ):
                continue

            x, y, w, h = det["bbox"]

            # Scale back
            x = int(x / SCALE)
            y = int(y / SCALE)
            w = int(w / SCALE)
            h = int(h / SCALE)

            # Clamp
            x = max(0, min(x, w_frame))
            y = max(0, min(y, h_frame))

            w = max(0, min(w, w_frame - x))
            h = max(0, min(h, h_frame - y))

            if not is_valid_face_size(
                w,
                h,
                MIN_FACE_SIZE,
            ):
                continue

            face_crop = frame[y : y + h, x : x + w]

            if face_crop.size == 0:
                continue

            current_name = self.last_recognition["name"]
            current_score = self.last_recognition["score"]
            current_emotion = self.last_emotion["emotion"]
            emotion_score = self.last_emotion["score"]

            if frame_count % RECOGNITION_INTERVAL == 0:

                try:

                    embedding = self.recognizer.get_embedding(face_crop)

                    current_name, current_score = self.recognizer.recognize(
                        embedding,
                        self.known_faces,
                    )

                    self.last_recognition = {
                        "name": current_name,
                        "score": current_score,
                    }

                except Exception as e:

                    print(f"Recognition error: {e}")

            if frame_count % EMOTION_INTERVAL == 0:
                try:
                    raw_emotion, emotion_score = (
                        self.emotion_classifier.predict_emotion(face_crop)
                    )

                    current_emotion = self.get_stable_emotion(raw_emotion)

                    self.last_emotion = {
                        "emotion": current_emotion,
                        "score": emotion_score,
                    }

                except Exception as e:
                    print(f"Emotion error: {e}")

            self.faces.append(
                {
                    "bbox": [x, y, w, h],
                    "name": current_name,
                    "score": current_score,
                    "emotion": current_emotion,
                    "emotion_score": emotion_score,
                }
            )

        return self.faces
