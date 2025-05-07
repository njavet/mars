from pydantic import BaseModel


class QueryRequest(BaseModel):
    base_url: str
    lm_name: str
    system_message: str
    query: str


class RagDocument(BaseModel):
    text: str
    source: str
    page_number: int
    distance: float = -1.0


class Evaluation(BaseModel):
    server: str
    filename: str
    system_message: str
    lm_names: list[str] = []
    outputs: list[str] = []
