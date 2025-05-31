from pydantic import BaseModel, Field


class EvalDoc(BaseModel):
    run: int
    server: str
    filename: str
    system_message: str
    models: dict[str, str]


class ScoreEntry(BaseModel):
    run: int = Field(..., ge=0)
    filename: str = Field(..., min_length=1)
    model_name: str = Field(..., min_length=1)
    scores: dict[str, int]


class Message(BaseModel):
    role: str
    content: str
