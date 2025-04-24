from pathlib import Path
import pdfplumber

# project imports
from mars.conf import PDF_DIR
from mars.data.tables import Sentence


def extract_pdfs() -> list[Sentence]:
    sentences = []
    for i, pdf_path in enumerate(PDF_DIR.glob('*.pdf')):
        try:
            new_sentences = extract_pages_with_metadata(pdf_path)
        except Exception as e:
            print(f'exception for {i}', e)
        else:
            sentences.extend(new_sentences)
    return sentences


def split_text(text: str, chunk_size: int = 512, overlap: int = 32) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def extract_pages_with_metadata(pdf_path: Path) -> list[Sentence]:
    sentences = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            cleaned_text = text_cleaning(text)
            for chunk in split_text(cleaned_text):
                sentence = Sentence(text=chunk,
                                    source=pdf_path.name,
                                    page_number=i)
                sentences.append(sentence)
    return sentences


def text_cleaning(text: str) -> str:
    """ remove newlines, too many whitespaces """
    # remove header and footer
    t0 = text.replace('\n', ' ')
    t1 = ' '.join(t0.split())
    return t1
