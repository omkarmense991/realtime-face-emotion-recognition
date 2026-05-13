# src/emotion/classifier.py

from deepface import DeepFace


class EmotionClassifier:
    """
    Emotion classification service.

    Uses DeepFace emotion analysis
    to predict dominant facial
    emotion and confidence score
    from detected face crops.

    Includes confidence thresholding
    to suppress weak predictions.
    """

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
