"""Data schematics for bot endpoints."""

from pydantic import BaseModel, Field


class UserInput(BaseModel):
    """Represents the data sent by the user to the bot."""

    user_msg: str = Field(..., example="Hi bot! What time is it?")
