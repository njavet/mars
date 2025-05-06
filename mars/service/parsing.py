import re


tools.display_dataframe_to_user(name="Parsed Sections", dataframe=pd.DataFrame(parsed_sections.items(), columns=["Section", "Content"]))


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

