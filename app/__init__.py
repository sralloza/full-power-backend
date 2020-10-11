from fastapi import FastAPI

from . import bot, users

app = FastAPI(
    title="Health Bot API", description="Backend for Health Bot", version="1.0.0a1"
)

app.include_router(bot.router)
app.include_router(users.router)
