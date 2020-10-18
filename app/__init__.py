"""Backend of chatbot application."""

import os

from fastapi import Depends, FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware

from . import bot, conversations, security, users
from ._version import get_versions
from .database import engine, models
from .security.utils import get_current_user

__version__ = get_versions()["version"]
del get_versions

models.Base.metadata.create_all(bind=engine)


fastapi_kwargs = dict(
    title="Health Bot API", description="Backend for Health Bot", version=__version__
)

if os.getenv("PRODUCTION"):
    fastapi_kwargs.update(docs_url=None, redoc_url=None)

app = FastAPI(**fastapi_kwargs)


app.include_router(security.router, tags=["security"])

app.include_router(bot.router, dependencies=[Depends(get_current_user)], tags=["bot"])

app.include_router(
    conversations.router,
    prefix="/conversations",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    tags=["conversations"],
)

# Users dependencies are defined for each route, because
# /users/me doesn't need the admin scope
app.include_router(users.router, tags=["users"], prefix="/users")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
