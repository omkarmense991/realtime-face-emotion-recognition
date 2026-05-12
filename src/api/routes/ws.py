import base64
import cv2
import numpy as np

from fastapi import (
    APIRouter,
    WebSocket,
)

from src.api.dependencies import (
    processor,
)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):

    await websocket.accept()

    while True:

        try:

            data = await websocket.receive_text()

            image_data = data.split(",")[1]

            image_bytes = base64.b64decode(image_data)

            np_array = np.frombuffer(
                image_bytes,
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

            await websocket.send_json({"faces": results})

        except Exception as e:

            print(f"WebSocket error: {e}")

            break
