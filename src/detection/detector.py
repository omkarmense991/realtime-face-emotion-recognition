import cv2
import mediapipe as mp


class FaceDetector:

    def __init__(self):

        self.mp_face_detection = mp.solutions.face_detection

        self.detector = self.mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5,
        )

    def detect(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        results = self.detector.process(rgb_frame)

        detections = []

        if not results.detections:
            return detections

        h, w, _ = frame.shape

        for detection in results.detections:

            bbox = detection.location_data.relative_bounding_box

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)

            width = int(bbox.width * w)
            height = int(bbox.height * h)

            confidence = detection.score[0]

            x = max(0, x)
            y = max(0, y)

            detections.append(
                {
                    "bbox": [
                        x,
                        y,
                        width,
                        height,
                    ],
                    "confidence": confidence,
                }
            )

        return detections
