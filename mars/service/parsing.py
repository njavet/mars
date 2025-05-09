from docx import Document
from docx.oxml.ns import qn

# project imports
from mars.conf.conf import ALLOWED_HEADINGS


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

