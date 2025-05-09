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
    chat_api: bool
    system_prompt_injection: str
    # TODO better a dict with {'lm_name': 'lm_name', 'output': 'output'} ?
    lms: dict[str, str]


class ScoreEntry(BaseModel):
    run: int
    filename: str
    lm_name: str
    scores: dict[str, str]
