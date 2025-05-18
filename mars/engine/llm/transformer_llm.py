from fastapi.logger import logger
from transformers import AutoTokenizer, AutoModelForCausalLM


# project imports
from mars.schema.llm import Message


class TransformerLLM:
    def __init__(self, model_name: str):
        ...
tokenizer = AutoTokenizer.from_pretrained('teknium/OpenHermes-2.5-Mistral-7B')
model = AutoModelForCausalLM.from_pretrained('teknium/OpenHermes-2.5-Mistral-7B')

