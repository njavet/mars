import tomli

# project imports
from mars.conf import PROMPT_PATH


def get_prompt(fname=PROMPT_PATH):
    with open(fname, 'rb') as f:
        config = tomli.load(f)

    prompt = config["prompts"]["evaluation"]
    return prompt


def get_full_prompt(prompt, doc_text):
    full_prompt = prompt.format(doc_text=doc_text)
    return full_prompt
