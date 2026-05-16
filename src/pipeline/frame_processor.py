# src/pipeline/frame_processor.py

import cv2

from src.pipeline.filters import (
    is_valid_detection,
    is_valid_face_size,
)

from src.config.settings import (
    DEBUG_TIMING,
    SCALE,
    DETECTION_INTERVAL,
    RECOGNITION_INTERVAL,
    EMOTION_INTERVAL,
    MIN_CONFIDENCE,
    MIN_FACE_SIZE,
)

from collections import deque, Counter

import time
from src.tracking.centroid_tracker import (
    CentroidTracker,
)


class FrameProcessor:
    """
    Central realtime inference pipeline.

    Responsibilities:
    - Face detection
    - Face tracking
    - Face recognition
    - Emotion classification
    - Per-face state management
    - Emotion smoothing

    Processes webcam frames and returns
    structured face inference results
    for rendering and streaming.
    """

    def __init__(
        self,
        detector,
        recognizer,
        database,
        emotion_classifier,
    ):

        self.detector = detector
        self.recognizer = recognizer
        self.database = database
        # Lazy-loaded after app startup
        # to avoid querying DB before
        # tables are created.
        self.known_faces = {}
        self.emotion_classifier = emotion_classifier

        self.face_states = {}

        self.faces = []

        self.emotion_histories = {}

        self.tracker = CentroidTracker()

    def get_stable_emotion(self, track_id, emotion):

        if track_id not in self.emotion_histories:
            self.emotion_histories[track_id] = deque(maxlen=3)

        self.emotion_histories[track_id].append(emotion)

        emotion_counts = Counter(self.emotion_histories[track_id])

        stable_emotion = emotion_counts.most_common(1)[0][0]

        return stable_emotion

    def reload_known_faces(self):
        self.known_faces = self.database.load_all_embeddings()

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

        if frame_count is not None and frame_count % DETECTION_INTERVAL != 0:
            return self.faces
        # Lazy-load embeddings after
        # application startup.
        if not self.known_faces:
            self.reload_known_faces()
        pipeline_start = time.time()

        detection_start = time.time()

        detections = self.detector.detect(small_frame)

        detection_time = time.time() - detection_start
        if DEBUG_TIMING:
            print(f"Detection: " f"{detection_time:.3f}s")

        detections = self.tracker.update(detections)

        active_ids = self.tracker.active_track_ids

        self.face_states = {
            track_id: state
            for track_id, state in self.face_states.items()
            if track_id in active_ids
        }

        self.emotion_histories = {
            track_id: history
            for track_id, history in self.emotion_histories.items()
            if track_id in active_ids
        }

        self.faces = []

        h_frame, w_frame = frame.shape[:2]

        for det in detections:

            if not is_valid_detection(
                det,
                MIN_CONFIDENCE,
            ):
                continue

            x, y, w, h = det["bbox"]
            track_id = det["track_id"]

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

            if track_id not in self.face_states:
                self.face_states[track_id] = {
                    "name": "Unknown",
                    "recognition_score": 0,
                    "emotion": "neutral",
                    "emotion_score": 0,
                }

            current_name = self.face_states[track_id]["name"]

            current_recognition_score = self.face_states[track_id]["recognition_score"]

            current_emotion = self.face_states[track_id]["emotion"]

            current_emotion_score = self.face_states[track_id]["emotion_score"]

            should_run_recognition = (
                frame_count is None or frame_count % RECOGNITION_INTERVAL == 0
            )

            if should_run_recognition:

                try:
                    recognition_start = time.time()
                    embedding = self.recognizer.get_embedding(face_crop)

                    current_name, current_recognition_score = self.recognizer.recognize(
                        embedding,
                        self.known_faces,
                    )

                    recognition_time = time.time() - recognition_start
                    if DEBUG_TIMING:
                        print(f"Recognition: " f"{recognition_time:.3f}s")

                    self.face_states[track_id]["name"] = current_name

                    self.face_states[track_id][
                        "recognition_score"
                    ] = current_recognition_score

                except Exception as e:

                    print(f"Recognition error: {e}")

            should_run_emotion = (
                frame_count is None or frame_count % EMOTION_INTERVAL == 0
            )

            if should_run_emotion:
                try:

                    emotion_start = time.time()
                    raw_emotion, current_emotion_score = (
                        self.emotion_classifier.predict_emotion(face_crop)
                    )

                    emotion_time = time.time() - emotion_start
                    if DEBUG_TIMING:
                        print(f"Emotion: " f"{emotion_time:.3f}s")

                    current_emotion = self.get_stable_emotion(track_id, raw_emotion)

                    self.face_states[track_id]["emotion"] = current_emotion

                    self.face_states[track_id]["emotion_score"] = current_emotion_score

                except Exception as e:
                    print(f"Emotion error: {e}")

            current_name = self.face_states[track_id]["name"]

            current_recognition_score = self.face_states[track_id]["recognition_score"]

            current_emotion = self.face_states[track_id]["emotion"]

            current_emotion_score = self.face_states[track_id]["emotion_score"]

            self.faces.append(
                {
                    "track_id": track_id,
                    "bbox": [x, y, w, h],
                    "name": current_name,
                    "recognition_score": current_recognition_score,
                    "emotion": current_emotion,
                    "emotion_score": current_emotion_score,
                }
            )

        pipeline_time = time.time() - pipeline_start
        if DEBUG_TIMING:
            print(f"Total pipeline: " f"{pipeline_time:.3f}s")

        return self.faces
