from fastapi.logger import logger
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig


# project imports
from mars.schema.llm import Message


class TransformerLLM:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = self.init_model()

    def init_model(self):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='fp4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        max_mem = {0: '7GiB', 'cpu': '28GiB'}

        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map='auto',
            max_memory=max_mem,
            torch_dtype=torch.bfloat16,
            quantization_config=bnb_config,
        )
        return model

    @torch.inference_mode
    def chat(self, messages: list[Message]) -> str:
        encoded = self.tokenizer.apply_chat_template(
            [msg.model_dump() for msg in messages],
            return_tensors='pt',
            truncation=True
        )
        input_ids = encoded.to(self.model.device)
        output_ids = self.model.generate(
            input_ids=input_ids,
            max_new_tokens=64,
            do_sample=False,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
            use_cache=False
        )
        generated = output_ids[0, input_ids.shape[-1]:]
        return self.tokenizer.decode(generated, skip_special_tokens=True)
