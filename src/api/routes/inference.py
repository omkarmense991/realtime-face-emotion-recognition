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
                "score": round(
                    f["score"],
                    2,
                ),
                "emotion": f["emotion"],
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
