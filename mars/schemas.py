from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    lm_name: str
    base_url: str


class SentenceSpec(BaseModel):
    faiss_index: int
    text: str
    source: str
    page_number: int


class RagDocument(BaseModel):
    text: str
    source: str
    page_number: int
    distance: float = -1.0


class AugmentedQuery(BaseModel):
    prompt: str
    rag_docs: list[RagDocument]
    system_message: str
