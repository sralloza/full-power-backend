"""Data schematics for bot endpoints."""

from pydantic import BaseModel, constr


class Msg(BaseModel):
    msg: constr(min_length=1)


class DFResponse(BaseModel):
    bot_msg: str
    intent: str
    is_end: bool
    parameters: dict
