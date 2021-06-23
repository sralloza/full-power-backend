from typing import Dict, List

from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class ErrorMessage(Message):
    pass


class Version(BaseModel):
    version: str


def gen_responses(responses: Dict[int, str], ignore: List[int] = None):
    ignore = ignore or list()
    data = {}

    for code, reason in responses.items():
        data[code] = {"description": reason}
        if code not in ignore: # noqa
            data[code]["model"] = ErrorMessage

    return {"responses": data}
