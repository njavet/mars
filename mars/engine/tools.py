import re
from difflib import get_close_matches

# project imports
from mars.schema.eval import Message
from mars.engine.prompts.medical import justifier_prompt


def extract_section_content(md_report: str, section: str) -> str:
    """
    Attempt to extract the content of a section using fuzzy matching.
    """

    header_matches = list(re.finditer(r'^##\s+(.+?)\s*$', md_report, flags=re.MULTILINE))

    headers = [m.group(1) for m in header_matches]
    print('headers:', headers)

    best_match = get_close_matches(section, headers, n=1, cutoff=0.6)
    if not best_match:
        print(f'no best match found for section: {section}')
        return ''

    correct_header = best_match[0]

    pattern = rf'## {re.escape(correct_header)}\n(.*?)(?=\n## |\Z)'
    match = re.search(pattern, md_report, flags=re.DOTALL)
    mm = match.group(0).strip()
    print('match', mm)
    return mm if match else ''


def justify_missing_section(llm, content: str) -> str:
    """
    Use another LLM to justify why the section is incomplete.
    """

    messages = [Message(role='system', content=justifier_prompt),
                Message(role='user', content=content)]

    llm.params['temperature'] = 0.7
    res = llm.chat(messages)
    return res
