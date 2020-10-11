from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import bot, users

load_dotenv()
app = FastAPI(
    title="Health Bot API", description="Backend for Health Bot", version="1.0.0a1"
)

app.include_router(bot.router, dependencies=[Depends(users.get_current_user)])
app.include_router(users.router)

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
