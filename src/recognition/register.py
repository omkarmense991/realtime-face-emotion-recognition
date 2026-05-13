# src/recognition/register.py

import cv2

from src.detection.detector import FaceDetector
from src.recognition.recognizer import FaceRecognizer
from src.recognition.database import FaceDatabase

MAX_SAMPLES = 10
CAPTURE_INTERVAL = 15
MIN_FACE_SIZE = 100


def register_user(name):

    cap = cv2.VideoCapture(0)

    detector = FaceDetector()
    recognizer = FaceRecognizer()
    database = FaceDatabase()

    embeddings = []

    frame_count = 0

    print(f"\nRegistering user: {name}")
    print(f"Capturing {MAX_SAMPLES} face samples...")
    print("Move your face slightly while capturing.")
    print("Press ESC to exit.\n")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        detections = detector.detect(frame)

        if detections:
            detections = [max(detections, key=lambda d: d["bbox"][2] * d["bbox"][3])]

        for det in detections:

            if det["confidence"] < 0.90:
                continue

            x, y, w, h = det["bbox"]

            if w < MIN_FACE_SIZE or h < MIN_FACE_SIZE:
                continue

            face_crop = frame[y : y + h, x : x + w]

            if face_crop.size == 0:
                continue

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Capture embedding every N frames
            if frame_count % CAPTURE_INTERVAL == 0:

                try:
                    embedding = recognizer.get_embedding(face_crop)

                    embeddings.append(embedding)

                    print(f"Captured sample " f"{len(embeddings)}/{MAX_SAMPLES}")

                except Exception as e:
                    print(f"Embedding error: {e}")

            # Stop after enough samples
            if len(embeddings) >= MAX_SAMPLES:

                database.save_embeddings(name, embeddings)

                print(f"\nSaved {len(embeddings)} embeddings for {name}")

                cap.release()
                cv2.destroyAllWindows()

                return

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    user_name = input("Enter user name: ")

    register_user(user_name)
