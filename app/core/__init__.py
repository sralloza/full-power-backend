import logging
from logging.handlers import TimedRotatingFileHandler
from uuid import uuid4

from starlette.responses import JSONResponse

from .config import settings

logger = logging.getLogger(__name__)


def setup_logging():
    fmt = "[%(asctime)s] %(levelname)s - %(name)s:%(lineno)s - %(message)s"
    # fmt = "[%(asctime)s] %(levelname)s - %(threadName)s.%(module)s:%(lineno)s - %(message)s"

    file_handler = TimedRotatingFileHandler(
        settings.log_path,
        when="midnight",
        encoding="utf-8",
        backupCount=settings.max_logs,
    )

    if file_handler.shouldRollover(None):
        file_handler.doRollover()

    logging.basicConfig(
        handlers=[file_handler],
        level=settings.logging_level.as_python_logging(),
        format=fmt,
    )

    logging.getLogger("asyncio").setLevel(50)
    logging.getLogger("multipart").setLevel(50)
    logging.getLogger("passlib").setLevel(50)
    logging.getLogger("werkzeug").setLevel(50)

def catch_errors(request, exc):
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
