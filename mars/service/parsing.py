import re
from docx import Document
from docx.oxml.ns import qn

# project imports
from mars.conf.conf import ALLOWED_HEADINGS


def parse_system_message(sm: str) -> str:
    # remove leading and training ws
    sm = '\n'.join(line.strip() for line in sm.splitlines())
    # replace tabs
    sm = re.sub(r'\t+', ' ', sm)
    # replace multiple ws with one ws
    sm = re.sub(r'[ ]{2,}', ' ', sm)
    # replace 3+ newlines with 2
    sm = re.sub(r'\n{3,}', '\n\n', sm)
    # replace non semantic newlines
    sm = re.sub(r'(?<!\n)\n(?!\n)', ' ', sm)
    # restore bullet point list
    sm = re.sub(r'(?<!\n)\* ', r'\n* ', sm)
    sm = '\n'.join(line.strip() for line in sm.splitlines())
    return sm


def strip_headers_footers(doc: Document) -> None:
    for sect in doc.sections:
        for tag in ('headerReference', 'footerReference'):
            for ref in sect._sectPr.findall(qn(f'w:{tag}')):
                sect._sectPr.remove(ref)
        for part in (
            sect.header, sect.first_page_header, sect.even_page_header,
            sect.footer, sect.first_page_footer, sect.even_page_footer
        ):
            part._element.clear()


def clean_medical_body(doc) -> dict[str, list[str]]:
    strip_headers_footers(doc)

    out: dict[str, list[str]] = {}
    current = None

    for p in doc.paragraphs:
        if p.part is not doc.part:
            continue
        text = p.text.strip()
        if not text:
            continue

        # new section ?
        if text in ALLOWED_HEADINGS:
            current = text
            out[current] = []
            continue

        if current:
            out[current].append(text)

    return {k: v for k, v in out.items() if v}
