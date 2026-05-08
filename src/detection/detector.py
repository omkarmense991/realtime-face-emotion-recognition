# src/detection/detector.py

from mtcnn import MTCNN
import cv2


class FaceDetector:
    def __init__(self):
        self.detector = MTCNN()

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = self.detector.detect_faces(rgb_frame)

        results = []

        for det in detections:
            x, y, w, h = det["box"]
            confidence = det["confidence"]

            # Fix negative values
            x, y = max(0, x), max(0, y)

            face_crop = frame[y : y + h, x : x + w]

            # Skip invalid crops
            if face_crop.size == 0:
                continue

            results.append({"bbox": [x, y, w, h], "confidence": confidence})

        return results
