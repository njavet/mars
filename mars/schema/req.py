from pydantic import BaseModel


class LLMSpec(BaseModel):
    base_url: str
    model: str
    system_message: str
    user_message: str
    chat_api: bool = True
    mode: str = 'base'
    tools: list[str] = []


class SystemMessage(BaseModel):
    key: str
    text: str
