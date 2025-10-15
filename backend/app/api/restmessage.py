from pydantic import BaseModel


class RestMessage(BaseModel):
    role: str
    text: str

class DeepChatRequest(BaseModel):
    messages: list[RestMessage]

class DeepChatResponse(BaseModel):
    text: str
