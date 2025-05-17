import re

# project imports
from mars.prompts import prompts, medical
from mars.schemas import SystemMessage


def load_system_messages():
    lst = []
    for name in dir(medical):
        if not name.startswith('_'):
            text = getattr(medical, name)
            sm = SystemMessage(key=name,
                               text=text)
            lst.append(sm)
    for name in dir(prompts):
        if not name.startswith('_'):
            text = getattr(prompts, name)
            sm = SystemMessage(key=name,
                               text=text)
            lst.append(sm)
    return lst


def format_medical_report(text, headers):
    sections = {}
    pattern = '|'.join([re.escape(h) for h in headers])
    matches = list(re.finditer(rf'(?P<header>{pattern})\s*\n', text))

    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        header = match.group('header')
        content = text[start:end].strip()
        sections[header] = content

    return sections
