from pydantic import BaseModel


class LLMRequest(BaseModel):
    base_url: str
    model: str
    system_message: str
    user_message: str
    chat_api: bool = True
    mode: str = 'base'
    tools: list[str] = []
