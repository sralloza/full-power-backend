from fastapi import APIRouter, Depends, Security

from app.api.dependencies.security import get_current_user

from . import bot, conversations, login, users

router = APIRouter()

router.include_router(login.router, tags=["security"])
router.include_router(
    bot.router, dependencies=[Depends(get_current_user)], tags=["bot"]
)
router.include_router(
    conversations.router,
    prefix="/conversations",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    tags=["conversations"],
)

# Users dependencies are defined for each route, because
# /users/me doesn't need the admin scope
router.include_router(users.router, tags=["users"], prefix="/users")
