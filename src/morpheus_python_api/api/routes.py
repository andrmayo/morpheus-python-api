from fastapi import APIRouter, Request

router = APIRouter()


@router.put("/latin", tags=["users"])
async def set_language_latin(request: Request) -> None:
    request
    return
