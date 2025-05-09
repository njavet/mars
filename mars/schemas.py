from pydantic import BaseModel, Field, field_validator

# project imports
from mars.conf.conf import SCORE_KEYS


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
    system_message_role: str
    # TODO better a dict with {'lm_name': 'lm_name', 'output': 'output'} ?
    lms: dict[str, str]


class ScoreEntry(BaseModel):
    run: int = Field(..., ge=0)
    filename: str = Field(..., min_length=1)
    lm_name: str = Field(..., min_length=1)
    scores: dict[str, str]

    @field_validator('scores')
    def check_scores(cls, v):
        if not v:
            raise ValueError('scores must not be empty')
        if sorted(v.keys()) != sorted(SCORE_KEYS):
            raise ValueError('scores must have keys {}'.format(SCORE_KEYS))
        if sorted(v.values()) != sorted(['yes', 'no']):
            raise ValueError('scores must be yes or no')
