from pydantic import BaseModel


class QueryRequest(BaseModel):
    server: str
    lm_name: str
    system_message: str
    query: str


class RagDocument(BaseModel):
    text: str
    source: str
    page_number: int
    distance: float = -1.0
