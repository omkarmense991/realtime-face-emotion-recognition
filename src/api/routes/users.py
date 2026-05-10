from typing import List

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
)

from src.api.dependencies import (
    database,
)
from src.services.user_services import UserService

from src.api.dependencies import (
    processor,
)

router = APIRouter()

user_service = UserService()


@router.get("/users/list")
def get_users():

    users = database.list_users()

    return {"users": users}


@router.delete("/users/delete/{name}")
def delete_user(name: str):

    database.delete_user(name)

    processor.reload_known_facess()

    return {"message": f"{name} deleted"}


@router.post("/users/register")
async def register_user(
    name: str = Form(...),
    files: List[UploadFile] = File(...),
):

    result = user_service.register_user(
        name,
        files,
    )

    processor.reload_known_facess()

    return result
