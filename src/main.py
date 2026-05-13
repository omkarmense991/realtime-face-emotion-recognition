# src/main.py

import cv2

from src.detection.detector import FaceDetector
from src.recognition.recognizer import FaceRecognizer
from src.recognition.database import FaceDatabase
from src.emotion.classifier import EmotionClassifier

from src.pipeline.frame_processor import FrameProcessor


def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: cannot access webcam")
        return

    detector = FaceDetector()
    recognizer = FaceRecognizer()
    database = FaceDatabase()
    emotion_classifier = EmotionClassifier()

    processor = FrameProcessor(
        detector=detector,
        recognizer=recognizer,
        database=database,
        emotion_classifier=emotion_classifier,
    )

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        faces = processor.process(
            frame,
            frame_count,
        )

        for f in faces:

            x, y, w, h = f["bbox"]

            name = f["name"]
            emotion = f["emotion"]

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"{name} : {emotion}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

        cv2.imshow(
            "Real-Time Face Recognition",
            frame,
        )

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
