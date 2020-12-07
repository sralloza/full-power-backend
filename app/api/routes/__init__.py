"""Routes router."""

from fastapi import APIRouter, Depends, Security

from app.api.dependencies.security import get_current_user

from . import bot, conversations, files, health_data, images, login, users, utils

router = APIRouter()

# security routes can be accessed by anyone (/login, /register, /refresh)
router.include_router(login.router, tags=["security"])

# utils routes can be accessed (almost) by anyone (/version)
# some routes need admin (like /settings) and others a normal user (/me)
router.include_router(utils.router, tags=["utils"])

# bot routes require a normal user
router.include_router(
    bot.router, dependencies=[Depends(get_current_user)], prefix="/bot", tags=["bot"]
)

# conversation routes require admin access
router.include_router(
    conversations.router,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    prefix="/conversations",
    tags=["conversations"],
)

# health-data routes require admin access
router.include_router(
    health_data.router,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    prefix="/health-data",
    tags=["health-data"],
)

# users routes require admin access
router.include_router(
    users.router,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    prefix="/users",
    tags=["users"],
)

# some user routes require admin access (create, update and remove), the rest are public
router.include_router(images.router, prefix="/images", tags=["images"])

# some files routes require admin access (create, update and remove), the rest are public
router.include_router(files.router, prefix="/files", tags=["files"])
