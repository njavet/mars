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


class EvalDoc(BaseModel):
    run: int
    server: str
    filename: str
    system_message: str
    lms: dict[str, str]
    chat_api: bool
    system_prompt_injection: str


class ScoreEntry(BaseModel):
    run: int
    filename: str
    lm_name: str
    scores: dict[str, str]
