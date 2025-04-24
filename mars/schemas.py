from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    lm_name: str
    base_url: str


class RagDocument(BaseModel):
    text: str
    source: str
    page_number: int
    distance: float = -1.0
