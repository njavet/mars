import tomli

# project imports
from mars.conf import PROMPT_PATH


def load_preprompts(fname=PROMPT_PATH):
    with open(fname, 'rb') as f:
        data = tomli.load(f)
    return data.get('preprompts', [])
