from fastapi import APIRouter, Request

from morpheus_python_api.types import Language

router = APIRouter()


@router.patch("/latin")
async def set_language_latin(request: Request) -> None:
    request.app.state.language = Language.LATIN
    return

@router.patch("/greek")
def set_language_greek(request: Request) -> None:
    request.app.state.language = Language.GREEK

@router.get("/parse/{text}")
async def parse(request: Request) -> str:

@router.post("/parse-cached/{text}")
async def parse_cached():
    return
