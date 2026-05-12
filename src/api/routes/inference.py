import cv2
import numpy as np

from fastapi import (
    APIRouter,
    UploadFile,
    File,
)

from src.api.dependencies import (
    processor,
)

# from src.db.database import (
#     SessionLocal,
# )

# from src.db.models import (
#     InferenceLog,
# )

router = APIRouter()


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):

    contents = await file.read()

    np_array = np.frombuffer(
        contents,
        np.uint8,
    )

    frame = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR,
    )

    faces = processor.process(
        frame,
        None,
    )

    results = []

    # db = SessionLocal()

    for f in faces:

        results.append(
            {
                "name": f["name"],
                "recognition_score": round(
                    f["recognition_score"] * 100,
                    1,
                ),
                "emotion": f["emotion"],
                "emotion_score": round(
                    f["emotion_score"],
                    1,
                ),
                "bbox": f["bbox"],
            }
        )

        # log = InferenceLog(
        #     name=f["name"],
        #     emotion=f["emotion"],
        #     score=float(f["score"]),
        # )

        # db.add(log)

    # db.commit()

    # db.close()

    return {"faces": results}
