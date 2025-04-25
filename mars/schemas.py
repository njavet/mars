from pydantic import BaseModel


class QueryRequest(BaseModel):
    base_url: str
    lm_name: str
    enable_rag: bool
    preprompt: str | None = None
    query: str


class RagDocument(BaseModel):
    text: str
    source: str
    page_number: int
    distance: float = -1.0
