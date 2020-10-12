import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import bot, conversations, security, users
from .database import engine, models

models.Base.metadata.create_all(bind=engine)

load_dotenv()

fastapi_kwargs = dict(
    title="Health Bot API", description="Backend for Health Bot", version="1.0.0a1"
)

if os.getenv("PRODUCTION", False):
    fastapi_kwargs.update(docs_url=None, redoc_url=None)

app = FastAPI(**fastapi_kwargs)


app.include_router(security.router, tags=["security"])
app.include_router(
    bot.router, dependencies=[Depends(security.get_current_user)], tags=["bot"]
)
app.include_router(
    conversations.router,
    dependencies=[Depends(security.get_current_user)],
    tags=["conversations"],
)
app.include_router(
    users.router, dependencies=[Depends(security.get_current_user)], tags=["users"]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
