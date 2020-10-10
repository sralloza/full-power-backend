from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic.fields import Field

app = FastAPI(
    title="Health Bot API", description="Backend for Health Bot", version="1.0.0a1"
)


class User(BaseModel):
    username: str
    password: str


valid_users = [("mark", "asdf"), ("user", "password")]
valid_users = [User(username=a, password=b) for (a, b) in valid_users]


class UserInput(BaseModel):
    user_input: str = Field(..., example="Hi bot! What time is it?")


class BotMessage(BaseModel):
    user_input: str = Field(..., example="Hi bot! What time is it?")
    bot_output: str = Field(..., example="Hi! It's 20:30.")


@app.post("/login")
def login_endpoint(user: User):
    """Login endpoint."""
    if user not in valid_users:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"status": "ok"}


@app.post("/logout")
def logout_endpoint():
    """Logout endpoint."""
    return "logout-endpoint"


@app.post("/bot-message", response_model=BotMessage)
def bot_messsage_endpoint(input_pack: UserInput):
    """Given a user input, returns the bot's response"""
    return BotMessage(user_input=input_pack.user_input, bot_output="bot-message")
