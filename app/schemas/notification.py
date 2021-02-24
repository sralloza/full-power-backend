from pydantic import BaseModel


class QuestionNotification(BaseModel):
    content: str
    id: str
