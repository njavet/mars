import tomli

# project imports
from mars.conf import PROMPT_PATH, SYS_PROMPT_PATH


def load_uiprompts(fname=PROMPT_PATH):
    with open(fname, 'rb') as f:
        data = tomli.load(f)
    return data.get('preprompts', [])


def load_system_prompt(name, fname=SYS_PROMPT_PATH):
    with open(fname, 'rb') as f:
        data = tomli.load(f)
    return data.get(name, '')
