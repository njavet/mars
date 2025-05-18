from pydantic import BaseModel


class LLMSpec(BaseModel):
    base_url: str | None = None
    model_name: str
    chat_mode: bool = True
    agentic: bool = False
    tools: list[str] = []
