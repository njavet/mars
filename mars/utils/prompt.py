import tomli

# project imports
from mars.conf import SYSTEM_PROMPT


def load_prompts(fname=SYSTEM_PROMPT):
    with open(fname, 'rb') as f:
        data = tomli.load(f)
    return data.get('system', [])
