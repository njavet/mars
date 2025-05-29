from pydantic import BaseModel


class LLMRequest(BaseModel):
    base_url: str | None = None
    model_name: str
    system_message: str
    user_message: str
    agentic: bool = False
