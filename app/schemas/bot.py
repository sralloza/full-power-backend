"""Data schematics for bot endpoints."""

from pydantic import BaseModel, constr, validator

from app.utils.translate import i18n


class DFResponse(BaseModel):
    bot_msg: str
    intent: str
    is_end: bool
    parameters: dict


class QuestionResponse(BaseModel):
    user_response: bool
    question_id: str

    @validator("question_id")
    def check_question_id(cls, v, values, config, field):
        if v.count(".") != 1:
            raise ValueError("question_id must have one dot ('.')")

        problem, pos = v.split(".")
        for user_response in ("true", "false"):
            try:
                i18n.t(f"response.{problem}.{user_response}.resp{pos}")
            except KeyError:
                raise ValueError("invalid question_id")

        return v
