"""
routes.py

FastAPI routes.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from typing import Annotated

from starlette.websockets import WebSocketDisconnected
from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.websockets import WebSocketState
from pydantic import StringConstraints, ValidationError

from morpheus_python_api.models import (
    CrunchOptions,
    ErrorMsg,
    CrunchMsg,
)
from morpheus_python_api.parse.parser import async_crunch
from morpheus_python_api.types import WordParse


logger = logging.getLogger(__name__)

_DISCONNECTS = (WebSocketDisconnect, WebSocketDisconnected)

router = APIRouter()


@router.get("/crunch_text/")
async def crunch_text(
    text: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, min_length=1, pattern=r"^\S+$"
        ),
    ],
    opts: Annotated[CrunchOptions, Query()],
    raise_on_failure: Annotated[bool, Query()] = False,
    failed_parse_output: Annotated[str | None, Query()] = None,
) -> str | WordParse:
    """Route for crunching a single input text.

    Args:
        text (str): query parameter for text to crunch.
        raw_cruncher_output (bool): If true, return raw cruncher output as a
            string. If false, return WordParse object. Defaults to False.
        opts: CrunchOptions object giving setting for cruncher.
        raise_on_failure (bool): if true, raise an HTTP 422 error for unparsable
            inputs. Defaults to False.
        failed_parse_output (str | None): output to return if parse fails. If
            None, input is echoed back. Does nothing if raise_on_failure = true.
            Defaults to None.

    Returns:
        A WordParse object if raw_cruncher_output = False, else the cruncher
            output as a string. Defaults to WordParse object.
    """
    try:
        result = [
            result
            async for result in async_crunch(
                text, **opts.model_dump(), raise_on_failure=False
            )
        ]
    except RuntimeError:
        raise HTTPException(status_code=503, detail="Cruncher unavailable")

    # handle unparsable inputs
    output = result[0]
    if output[0] == output[1]:
        if raise_on_failure:
            raise HTTPException(status_code=422, detail="Unparsable input")
        if failed_parse_output is not None:
            return failed_parse_output

    return output[1]


async def ws_lines(ws: WebSocket) -> AsyncIterator[str]:
    """Yield messages from the client until disconnect."""
    try:
        while True:
            line = await ws.receive_text()
            if line.strip():
                yield line
    except _DISCONNECTS:
        raise


async def _send_error(ws: WebSocket, msg: ErrorMsg):
    await ws.send_text(msg.model_dump_json())


@asynccontextmanager
async def _ws_session(ws: WebSocket):
    await ws.accept()
    try:
        yield
    except _DISCONNECTS:
        pass
    finally:
        with suppress(Exception):
            if ws.application_state is WebSocketState.CONNECTED:
                await ws.close()


def _error_msg(log_msg: str):
    return log_msg + ", see logs"


# Unlike for the crunch_text function above, error handling is largely
# left to the client. An ErrorMsg simply returns the information needed
# to handle different errors.
@router.websocket("/ws/crunch")
async def ws_crunch(
    ws: WebSocket,
):
    """Route for streaming crunches via a web socket.

    Note that the socket must first send a CrunchOptions message before sending
    input strings.
    """

    async with _ws_session(ws):
        try:
            opts = CrunchOptions.model_validate(await ws.receive_json())
        # This gets handled by context manager
        except _DISCONNECTS:
            raise
        except ValidationError:
            log_msg = "Invalid crunch options"
            logger.exception(log_msg)
            await _send_error(
                ws,
                ErrorMsg(type="validation", detail=_error_msg(log_msg)),
            )
            return
        except Exception:
            log_msg = "Encountered unexpected error"
            logger.exception(log_msg)
            await _send_error(
                ws, ErrorMsg(type="other", detail=_error_msg(log_msg))
            )
            return

        type_literal = "raw" if opts.raw_cruncher_output else "structured"
        try:
            async for result in async_crunch(
                ws_lines(ws), **opts.model_dump(), raise_on_failure=False
            ):
                if result[0] == result[1]:
                    await _send_error(
                        ws,
                        ErrorMsg(
                            type="unparsed",
                            word=result[0],
                            detail="Unparsable input",
                        ),
                    )
                    continue

                await ws.send_text(
                    CrunchMsg(
                        type=type_literal, word=result[0], parse=result[1]
                    ).model_dump_json()
                )
        # This gets handled by context manager
        except _DISCONNECTS:
            raise
        except RuntimeError:
            log_msg = "Cruncher unavailable"
            logger.exception(log_msg)
            await _send_error(
                ws,
                ErrorMsg(type="runtime", detail=_error_msg(log_msg)),
            )
        except Exception:
            log_msg = "Encountered unexpected error"
            logger.exception(log_msg)
            await _send_error(
                ws,
                ErrorMsg(
                    type="other",
                    detail=_error_msg(log_msg),
                ),
            )
