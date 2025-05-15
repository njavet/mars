from pydantic import BaseModel, Field, field_validator

# project imports
from mars.conf.conf import SCORE_KEYS, SCORE_VALUES


class SystemMessage(BaseModel):
    # TODO add format validation
    key: str
    text: str


class Message(BaseModel):
    role: str
    content: str
    lm_name: str | None = None


class QueryRequest(BaseModel):
    base_url: str
    lm_name: str
    system_message: str
    query: str
    chat_api: bool = True
    system_message_role: str = 'user'
    mode: str = 'base'
    tools: list[str] = []


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

    @field_validator('scores', mode='after')
    @classmethod
    def check_scores(cls, v: dict[str, str]) -> dict[str, str]:
        if not v:
            raise ValueError('scores must not be empty')
        if sorted(v.keys()) != sorted(SCORE_KEYS):
            raise ValueError('scores must have keys {}'.format(SCORE_KEYS))
        if not all(val in SCORE_VALUES for val in v.values()):
            raise ValueError('scores must be in {}'.format(SCORE_VALUES))
        return v
