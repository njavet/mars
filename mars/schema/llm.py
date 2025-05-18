from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class OpenHermes(BaseModel):
    name: str = 'OpenHermes'
    model: str = 'openhermes:latest'
    context_window: int = 32768
    params: dict = {
        'temperature': 0,
        'stop': ['<|im_start|>', '<|im_end|>'],
    }
    template: str = """
        <|im_start|>system
        {system}<|im_end|>
        <|im_start|>user
        {query}<|im_end|>
        <|im_start|>assistant
    """
