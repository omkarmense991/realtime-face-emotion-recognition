# src/recognition/database.py

from src.db.database import SessionLocal
from src.db.models import FaceEmbedding


class FaceDatabase:

    def save_embeddings(
        self,
        name,
        embeddings,
    ):

        db = SessionLocal()

        # Remove old embeddings
        db.query(FaceEmbedding).filter(FaceEmbedding.name == name).delete()

        for emb in embeddings:

            record = FaceEmbedding(
                name=name,
                embedding=emb,
            )

            db.add(record)

        db.commit()

        db.close()

    def load_all_embeddings(self):

        db = SessionLocal()

        rows = db.query(FaceEmbedding).all()

        database = {}

        for row in rows:

            if row.name not in database:
                database[row.name] = []

            database[row.name].append(row.embedding)

        db.close()

        return database

    def delete_user(self, name):

        db = SessionLocal()

        db.query(FaceEmbedding).filter(FaceEmbedding.name == name).delete()

        db.commit()

        db.close()

    def list_users(self):

        db = SessionLocal()

        rows = db.query(FaceEmbedding.name).distinct().all()

        db.close()

        return [r[0] for r in rows]
