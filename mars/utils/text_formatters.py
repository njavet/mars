import re


def format_as_markdown(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.replace('\n', '  \n')
