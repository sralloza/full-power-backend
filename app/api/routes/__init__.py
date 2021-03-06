"""Routes router."""

from fastapi import APIRouter

from . import (
    bot,
    conversations,
    files,
    health_data,
    images,
    notifications,
    security,
    users,
    utils,
)

router = APIRouter()

router.include_router(bot.router)
router.include_router(conversations.router)
router.include_router(files.router)
router.include_router(health_data.router)
router.include_router(images.router)
router.include_router(notifications.router)
router.include_router(security.router)
router.include_router(users.router)
router.include_router(utils.router)
