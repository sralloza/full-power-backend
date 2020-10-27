"""Data schematics for bot endpoints."""

from pydantic import BaseModel


class Msg(BaseModel):
    msg: str
