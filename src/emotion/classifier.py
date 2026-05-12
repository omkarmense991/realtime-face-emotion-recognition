# src/emotion/classifier.py

from deepface import DeepFace


class EmotionClassifier:

    def predict_emotion(
        self,
        face_image,
        threshold=85,
    ):

        result = DeepFace.analyze(
            img_path=face_image,
            actions=["emotion"],
            enforce_detection=False,
            silent=True,
        )

        emotion = result[0]["dominant_emotion"]

        confidence = result[0]["emotion"][emotion]

        if confidence < threshold:

            return (
                "uncertain",
                confidence,
            )

        return (
            emotion,
            confidence,
        )
