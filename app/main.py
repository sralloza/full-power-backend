"""Backend of chatbot application."""

from logging import getLogger

from fastapi import Depends, FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware

from . import __version__, bot, conversations, security, users
from .config import settings
from .database import engine, models
from .security.utils import get_current_user
from .utils import catch_errors

logger = getLogger(__name__)


def create_app():
    fastapi_kwargs = dict(
        title="Health Bot API",
        description="Backend for Health Bot",
        version=__version__,
    )

    if settings.production:
        fastapi_kwargs.update(openapi_url=None)

    api = FastAPI(**fastapi_kwargs)

    api.include_router(security.router, tags=["security"])

    api.include_router(
        bot.router, dependencies=[Depends(get_current_user)], tags=["bot"]
    )

    api.include_router(
        conversations.router,
        prefix="/conversations",
        dependencies=[Security(get_current_user, scopes=["admin"])],
        tags=["conversations"],
    )

    # Users dependencies are defined for each route, because
    # /users/me doesn't need the admin scope
    api.include_router(users.router, tags=["users"], prefix="/users")

    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api.add_exception_handler(500, catch_errors)

    models.Base.metadata.create_all(bind=engine)

    return api
