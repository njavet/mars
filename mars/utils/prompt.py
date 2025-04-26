import tomli

# project imports
from mars.conf import PROMPT_PATH, SYS_PROMPT_PATH


def load_prompts(fname=PROMPT_PATH):
    with open(fname, 'rb') as f:
        data = tomli.load(f)
    return data.get('preprompts', [])
