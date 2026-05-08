# src/recognition/recognizer.py

from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class FaceRecognizer:

    def __init__(self, model_name="Facenet"):

        self.model_name = model_name

    def get_embedding(self, face_image):

        embedding = DeepFace.represent(
            img_path=face_image, model_name=self.model_name, enforce_detection=False
        )

        return embedding[0]["embedding"]

    def compare_embeddings(self, embedding1, embedding2):

        emb1 = np.array(embedding1).reshape(1, -1)
        emb2 = np.array(embedding2).reshape(1, -1)

        similarity = cosine_similarity(emb1, emb2)[0][0]

        return similarity

    def recognize(self, embedding, database, threshold=0.65):

        best_match = "Unknown"
        best_score = -1

        for name, embeddings in database.items():

            for stored_embedding in embeddings:

                similarity = self.compare_embeddings(embedding, stored_embedding)

                if similarity > best_score:
                    best_score = similarity
                    best_match = name

        if best_score >= threshold:
            return best_match, best_score

        return "Unknown", best_score
