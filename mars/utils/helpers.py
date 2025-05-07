import json
import toml
from pathlib import Path
import re
from docx import Document

# project imports
from mars.conf.conf import SYSTEM_PROMPTS


def load_system_messages(filepath=SYSTEM_PROMPTS):
    system_prompts = toml.load(filepath)
    lst = []
    for key, attrs in system_prompts.items():
        s = ''
        for k, v in attrs.items():
            s += '{}: {}\n'.format(k, v)

        dix = {'key': key,
               'text': s}
        lst.append(dix)

    return lst


def format_as_markdown(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.replace('\n', '  \n')


def read_docx(docx_path: Path):
    doc = Document(docx_path)
    text = ''.join([para.text for para in doc.paragraphs])
    return text
