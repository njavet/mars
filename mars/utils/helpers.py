import os
import toml
from pathlib import Path
import re
from docx import Document

# project imports
from mars.conf.conf import SYSTEM_PROMPTS, RESULTS_DIR


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
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text


def get_number_of_runs():
    runs = len([d for d in os.listdir(RESULTS_DIR)
                if os.path.isdir(os.path.join(RESULTS_DIR, d))])
    return runs

