from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    lm_name: str
    base_url: str

