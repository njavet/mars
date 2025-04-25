import tomli

# project imports
from mars.conf import PROMPT_PATH


def get_prompt(prompt_mode: str, fname=PROMPT_PATH):
    with open(fname, 'rb') as f:
        config = tomli.load(f)

    prompt = config['prompts'][prompt_mode]
    return prompt
