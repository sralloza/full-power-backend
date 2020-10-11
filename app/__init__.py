from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, models

from . import bot, security, users

models.Base.metadata.create_all(bind=engine)

load_dotenv()
app = FastAPI(
    title="Health Bot API", description="Backend for Health Bot", version="1.0.0a1"
)


app.include_router(security.router, tags=["security"])
app.include_router(
    bot.router, dependencies=[Depends(security.get_current_user)], tags=["bot"]
)
app.include_router(
    users.router, dependencies=[Depends(security.get_current_user)], tags=["users"]
)

origins = [
    "https?://localhost:*",
    "https?://api.sralloza.es",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
