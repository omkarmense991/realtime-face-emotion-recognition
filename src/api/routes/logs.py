from fastapi import APIRouter

from src.db.database import (
    SessionLocal,
)

from src.db.models import (
    InferenceLog,
)

router = APIRouter()


@router.get("/logs")
def get_logs():

    db = SessionLocal()

    logs = (
        db.query(InferenceLog).order_by(InferenceLog.created_at.desc()).limit(20).all()
    )

    results = []

    for log in logs:

        results.append(
            {
                "id": log.id,
                "name": log.name,
                "emotion": log.emotion,
                "score": round(
                    log.score,
                    2,
                ),
                "created_at": log.created_at,
            }
        )

    db.close()

    return results
