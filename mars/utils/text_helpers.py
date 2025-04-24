from pathlib import Path
import pdfplumber


def extract_pdfs(doc_dir: Path) -> tuple[list, list]:
    texts = []
    metadatas = []
    for i, pdf_path in enumerate(doc_dir.glob('*.pdf')):
        try:
            new_texts, new_metadatas = extract_pages_with_metadata(pdf_path)
        except Exception as e:
            print(f'exception for {i}', e)
        else:
            texts.extend(new_texts)
            metadatas.extend(new_metadatas)
    return texts, metadatas


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


def extract_pages_with_metadata(pdf_path: Path) -> tuple[list, list]:
    texts = []
    metadatas = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            cleaned_text = text_cleaning(text)
            metadata = {'source': pdf_path.name, 'page_number': i}
            texts.append(cleaned_text)
            metadatas.append(metadata)
    return texts, metadatas


def text_cleaning(text: str) -> str:
    """ remove newlines, too many whitespaces """
    # remove header and footer
    t0 = text.replace('\n', ' ')
    t1 = ' '.join(t0.split())
    return t1
