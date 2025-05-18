from pydantic import BaseModel


class RagDocument(BaseModel):
    text: str
    source: str
    page_number: int
    distance: float = -1.0
