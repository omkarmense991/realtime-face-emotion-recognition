import cv2
import numpy as np

from src.api.dependencies import (
    detector,
    recognizer,
    database,
)


class UserService:

    def register_user(
        self,
        name,
        files,
    ):

        embeddings = []

        for file in files:

            contents = file.file.read()

            np_array = np.frombuffer(
                contents,
                np.uint8,
            )

            frame = cv2.imdecode(
                np_array,
                cv2.IMREAD_COLOR,
            )

            detections = detector.detect(frame)

            if not detections:
                continue

            det = max(detections, key=lambda d: d["bbox"][2] * d["bbox"][3])

            x, y, w, h = det["bbox"]

            face_crop = frame[
                y : y + h,
                x : x + w,
            ]

            embedding = recognizer.get_embedding(face_crop)

            embeddings.append(embedding)

        if not embeddings:

            return {"success": False, "message": "No valid faces found"}

        database.save_embeddings(
            name,
            embeddings,
        )

        return {
            "success": True,
            "message": f"{name} registered",
            "samples": len(embeddings),
        }
