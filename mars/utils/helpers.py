import toml
import re

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

