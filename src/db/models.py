# src/db/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
)

from datetime import datetime, timezone

from src.db.database import Base

from sqlalchemy import JSON


class InferenceLog(Base):

    __tablename__ = "inference_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(String)

    emotion = Column(String)

    score = Column(Float)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class FaceEmbedding(Base):

    __tablename__ = "face_embeddings"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
        index=True,
    )

    embedding = Column(JSON)
