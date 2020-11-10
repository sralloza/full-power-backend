"""Data schematics for bot endpoints."""

from pydantic import BaseModel, constr


class Msg(BaseModel):
    msg: constr(min_length=1)
