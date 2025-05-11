import re

# project imports
from mars.conf import prompts


def load_system_messages():
    lst = []
    for name in dir(prompts):
        if not name.startswith('_'):
            text = getattr(prompts, name)
            lst.append({'key': name,
                        'text': text})
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

