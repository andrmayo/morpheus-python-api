"""
routes.py

FastAPI routes.
"""

from collections.abc import AsyncIterator
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from morpheus_python_api.parse.parser import async_crunch
from morpheus_python_api.types import CrunchOptions

router = APIRouter()


@router.get("/crunch_text/{text}")
async def crunch_text(text: str) -> str:
    result = [result async for result in async_crunch(text)]
    return result[0]


async def ws_lines(ws: WebSocket) -> AsyncIterator[str]:
    """Yield messages from the client until disconnect."""
    try:
        while True:
            yield await ws.receive_text()
    except WebSocketDisconnect:
        return


@router.websocket("/ws/crunch")
async def ws_crunch(
    ws: WebSocket,
):
    await ws.accept()
    # NOTE: perhaps raise_on_failure should be false
    opts = CrunchOptions.model_validate(await ws.receive_json())
    # NOTE: probably catch failures
    async for result in async_crunch(ws_lines(ws), **opts.model_dump()):
        await ws.send_text(result)
    await ws.close()


# @router.post("/crunch-cached/{text}")
# async def parse_cached():
#     return
