from pydantic import BaseModel


class SystemMessage(BaseModel):
    key: str
    text: str
