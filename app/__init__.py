from fastapi import Depends, FastAPI

from . import bot, users

app = FastAPI(
    title="Health Bot API", description="Backend for Health Bot", version="1.0.0a1"
)

app.include_router(bot.router, dependencies=[Depends(users.get_current_user)])
app.include_router(users.router)
