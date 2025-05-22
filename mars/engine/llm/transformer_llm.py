from fastapi.logger import logger
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


# project imports
from mars.schema.llm import Message


class TransformerLLM:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = self.init_model()

    def init_model(self):
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map='auto',
            torch_dtype=torch.float16,
            load_in_4bit=True,
            llm_int8_enable_fp32_cpu_offload=True
        )
        return model

    def chat(self, messages: list[Message]) -> str:
        messages = [msg.model_dump() for msg in messages]
        inputs = self.tokenizer.apply_chat_template(
            messages,
            return_tensors='pt'
        ).to('cuda')
        gen_ids = self.model.generate(inputs, max_new_tokens=16)
        return self.tokenizer.batch_decode(gen_ids)[0]
