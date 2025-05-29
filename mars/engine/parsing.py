from pathlib import Path
import json
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

# project imports
from mars.core import conf


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


def split_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=conf.DOC_CHUNK_SIZE,
        chunk_overlap=0,
        separators=conf.DOC_SEPARATORS
    )
    chunks = splitter.split_text(text)
    return chunks


def flatten_sections(section_name, content):
    """
    Flatten a section: if it's a nested dict (with subsections),
    concatenate with headers. If it's a string, return as-is.
    """
    if isinstance(content, dict):
        combined = []
        for sub, text in content.items():
            combined.append(f'{sub}:\n{text.strip()}')
        return section_name, '\n\n'.join(combined)
    else:
        return section_name, content.strip()


def parse_all_json_sections(folder):
    """
    Parse all `.json` files in a folder,
    return list of (section_name, content) tuples.
    """
    results = []
    for file in Path(folder).glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for section, content in data.items():
                name, body = flatten_sections(section, content)
                results.append({
                    'file': file.name,
                    'section': name,
                    'content': body
                })
    return results
