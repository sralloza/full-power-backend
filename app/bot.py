from fastapi.routing import APIRouter
from pydantic import Field
from pydantic.main import BaseModel

router = APIRouter()


class UserInput(BaseModel):
    user_input: str = Field(..., example="Hi bot! What time is it?")


class BotMessage(BaseModel):
    user_input: str = Field(..., example="Hi bot! What time is it?")
    bot_output: str = Field(..., example="Hi! It's 20:30.")


@router.post("/bot-message", response_model=BotMessage)
def bot_messsage_endpoint(input_pack: UserInput):
    """Given a user input, returns the bot's response"""
    return BotMessage(user_input=input_pack.user_input, bot_output="bot-message")
