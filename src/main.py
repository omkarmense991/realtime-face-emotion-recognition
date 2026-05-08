# src/main.py

import cv2

from src.detection.detector import FaceDetector
from src.recognition.recognizer import FaceRecognizer
from src.recognition.database import FaceDatabase

# =========================
# Constants
# =========================

DETECTION_INTERVAL = 3
RECOGNITION_INTERVAL = 10

SCALE = 0.5

MIN_CONFIDENCE = 0.90
MIN_FACE_SIZE = 100


def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: cannot access webcam")
        return

    detector = FaceDetector()
    recognizer = FaceRecognizer()

    database = FaceDatabase()
    known_faces = database.load_all_embeddings()

    frame_count = 0

    faces = []

    # Persist last recognition result
    # (temporary solution until face tracking is added)
    last_recognition = {"name": "Unknown", "score": 0}

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Resize frame for faster detection
        small_frame = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)

        # =========================
        # Face Detection
        # =========================

        if frame_count % DETECTION_INTERVAL == 0:

            detections = detector.detect(small_frame)

            new_faces = []

            h_frame, w_frame = frame.shape[:2]

            # Keep only largest face
            if detections:
                detections = [
                    max(detections, key=lambda d: d["bbox"][2] * d["bbox"][3])
                ]

            for det in detections:

                if det["confidence"] < MIN_CONFIDENCE:
                    continue

                x, y, w, h = det["bbox"]

                # Scale back to original frame size
                x = int(x / SCALE)
                y = int(y / SCALE)
                w = int(w / SCALE)
                h = int(h / SCALE)

                # Clamp values
                x = max(0, min(x, w_frame))
                y = max(0, min(y, h_frame))

                w = max(0, min(w, w_frame - x))
                h = max(0, min(h, h_frame - y))

                # Reject very small faces
                if w < MIN_FACE_SIZE or h < MIN_FACE_SIZE:
                    continue

                # Extract face crop
                face_crop = frame[y : y + h, x : x + w]

                if face_crop.size == 0:
                    continue

                # Default recognition state
                current_name = last_recognition["name"]
                current_score = last_recognition["score"]

                # =========================
                # Face Recognition
                # =========================

                if frame_count % RECOGNITION_INTERVAL == 0:

                    try:

                        embedding = recognizer.get_embedding(face_crop)

                        current_name, current_score = recognizer.recognize(
                            embedding, known_faces
                        )

                        # Persist last successful result
                        last_recognition = {
                            "name": current_name,
                            "score": current_score,
                        }

                        print(f"{current_name} " f"({current_score:.2f})")

                    except Exception as e:

                        print(f"Recognition error: {e}")

                new_faces.append(
                    {
                        "bbox": [x, y, w, h],
                        "confidence": det["confidence"],
                        "name": current_name,
                        "score": current_score,
                    }
                )

            faces = new_faces

        # =========================
        # Rendering
        # =========================

        for f in faces:

            x, y, w, h = f["bbox"]

            name = f["name"]
            score = f["score"]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.putText(
                frame,
                f"{name} ({score:.2f})",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

        cv2.imshow("Real-Time Face Recognition", frame)

        # ESC key to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
