"""Useful functions for the entire application."""

from logging import FileHandler, basicConfig, getLogger
from pathlib import Path
from uuid import uuid4

from fastapi import Request
from starlette.responses import JSONResponse

from app.core.config import settings

logger = getLogger(__name__)


def setup_logging():
    fmt = "[%(asctime)s] %(levelname)s - %(name)s:%(lineno)s - %(message)s"

    Path(settings.log_path).parent.mkdir(parents=True, exist_ok=True)

    file_handler = FileHandler(settings.log_path, encoding="utf-8")

    basicConfig(
        handlers=[file_handler],
        level=settings.logging_level.as_python_logging(),
        format=fmt,
    )

    getLogger("asyncio").setLevel(50)
    getLogger("multipart").setLevel(50)
    getLogger("passlib").setLevel(50)
    getLogger("werkzeug").setLevel(50)


def catch_errors(request: Request, exc: Exception):
    """Logs an error and returns 500 to the user."""
    error_id = uuid4()
    scope = request.scope
    request_info = (
        f"[{request.client.host}] {scope['scheme'].upper()}/{scope['http_version']} "
        f"{scope['method']} {scope['path']}"
    )

    exc_info = (exc.__class__, exc, exc.__traceback__)
    logger.critical(
        "Unhandled exception [id=%s] in request '%s':",
        error_id,
        request_info,
        exc_info=exc_info,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error, please contact the server administrator."
        },
        headers={"X-Error-ID": str(error_id)},
    )
