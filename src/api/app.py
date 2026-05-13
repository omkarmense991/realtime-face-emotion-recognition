from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from src.db.database import engine

from src.db.models import Base

from src.api.routes.inference import (
    router as inference_router,
)

from src.api.routes.users import (
    router as users_router,
)

from src.api.routes.logs import (
    router as logs_router,
)

from src.api.routes.ws import (
    router as ws_router,
)

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():

    return {"status": "running"}


app.include_router(inference_router)

app.include_router(users_router)

app.include_router(logs_router)

app.include_router(ws_router)
