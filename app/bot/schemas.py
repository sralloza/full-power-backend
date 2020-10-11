from pydantic import BaseModel, Field


class UserInput(BaseModel):
    user_msg: str = Field(..., example="Hi bot! What time is it?")
