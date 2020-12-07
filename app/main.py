"""Backend of chatbot application."""

from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__, api
from .core.config import settings
from .utils import catch_errors

logger = getLogger(__name__)


def create_app()->FastAPI:
    """Creates the FastAPI app."""
    fastapi_kwargs = dict(
        title="Health Bot API",
        description="Backend for Health Bot",
        version=__version__,
    )

    if settings.production:
        fastapi_kwargs.update(dict(openapi_url=None))

    app = FastAPI(**fastapi_kwargs)
    app.include_router(api.router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(500, catch_errors)

    return app
