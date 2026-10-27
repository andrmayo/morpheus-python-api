"""
routes.py

FastAPI routes.
"""

from fastapi import APIRouter

from morpheus_python_api.parse.parser import async_crunch

router = APIRouter()


@router.get("/crunch/{text}")
async def crunch_text(text: str) -> str:
    result = await async_crunch(text)
    return result


@router.post("/crunch-cached/{text}")
async def parse_cached():
    return
