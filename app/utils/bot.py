from typing import List

from app.core.config import settings


def split_bot_msg(bot_msg: str) -> List[str]:
    bot_msg = bot_msg.replace("\n", settings.bot_split_char)
    return bot_msg.split(settings.bot_split_char)
