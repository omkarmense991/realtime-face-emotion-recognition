# src/api/app.py

import cv2
import numpy as np

from fastapi import FastAPI, UploadFile, File

from src.detection.detector import FaceDetector
from src.recognition.recognizer import FaceRecognizer
from src.recognition.database import FaceDatabase
from src.emotion.classifier import EmotionClassifier

from src.pipeline.frame_processor import FrameProcessor

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Initialize ML Components
# =========================

detector = FaceDetector()

recognizer = FaceRecognizer()

emotion_classifier = EmotionClassifier()

database = FaceDatabase()

processor = FrameProcessor(
    detector=detector,
    recognizer=recognizer,
    emotion_classifier=emotion_classifier,
    database=database,
)

frame_count = 0


# =========================
# Health Check
# =========================


@app.get("/")
def health():

    return {"status": "running"}


# =========================
# Analyze Frame Endpoint
# =========================


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):

    global frame_count

    contents = await file.read()

    np_array = np.frombuffer(
        contents,
        np.uint8,
    )

    frame = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR,
    )

    frame_count += 1

    faces = processor.process(
        frame,
        None,
    )

    results = []

    for f in faces:

        results.append(
            {
                "name": f["name"],
                "score": round(f["score"], 2),
                "emotion": f["emotion"],
                "bbox": f["bbox"],
            }
        )

    return {"faces": results}
