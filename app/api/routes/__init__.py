from fastapi import APIRouter, Depends, Security

from app.api.dependencies.security import get_current_user

from . import bot, conversations, login, users, utils

router = APIRouter()

router.include_router(login.router, tags=["security"])
router.include_router(utils.router, tags=["utils"])
router.include_router(
    bot.router, dependencies=[Depends(get_current_user)], tags=["bot"]
)
router.include_router(
    conversations.router,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    prefix="/conversations",
    tags=["conversations"],
)

router.include_router(
    users.router,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    prefix="/users",
    tags=["users"],
)
