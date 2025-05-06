import json
from pathlib import Path
import re
from docx import Document
import tomli

# project imports
from mars.conf import SYSTEM_PROMPT


def load_prompts(fname=SYSTEM_PROMPT):
    with open(fname, 'rb') as f:
        data = tomli.load(f)
    return data.get('system', [])


def format_as_markdown(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.replace('\n', '  \n')


def read_docx(docx_path: Path):
    doc = Document(docx_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text


def append_score_dict(filepath: Path):
    data = json.load(open(filepath))
    data.append({'scores': {'found': 0, 'added': 0}})
    json.dump(data, open(filepath, 'w'), indent=2, ensure_ascii=False)
