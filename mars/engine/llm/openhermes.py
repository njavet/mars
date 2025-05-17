from mars.engine.llm.base import BaseOllamaLLM


class OpenHermes(BaseOllamaLLM):
    def __init__(self, base_url: str) -> None:
        super().__init__(base_url=base_url,
                         name='OpenHermes',
                         model='openhermes:latest',
                         context_window=32768,
                         params={
                             'temperature': 0,
                             'stop': ['<|im_start', '<|im_end|>']
                         })
