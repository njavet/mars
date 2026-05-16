import json
import re


# TODO if a section separated with '\n\n' contains too many characters,
#  split into two sections with same title
def parse_text_to_llm_input(text: str) -> str:
    # remove leading and training ws
    text = '\n'.join(line.strip() for line in text.splitlines())
    # replace tabs
    text = re.sub(r'\t+', ' ', text)
    # replace multiple ws with one ws
    text = re.sub(r'[ ]{2,}', ' ', text)
    # replace 3+ newlines with 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    # replace non semantic newlines
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    # restore bullet point list
    text = re.sub(r'(?<!\n)\* ', r'\n* ', text)
    text = '\n'.join(line.strip() for line in text.splitlines())
    return text


def markdown_to_json(text: str) -> str:
    sections = text.split('\n\n')
    dix = {}
    for section in sections:
        m = re.match(r'##(?: [^\n]+){1,3}\n', section + '\n')
        header = m.group(0)
        tlen = len(header)
        dix[header[3:].strip()] = section[tlen:]
    return json.dumps(dix)
