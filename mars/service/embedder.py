from pathlib import Path
from fastapi.logger import logger
import numpy as np
import pdfplumber
import faiss
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

# project imports
from mars.conf import PDF_DIR, CHUNK_SIZE, OVERLAP
from mars.data.tables import Sentence


class EmbeddingService:
    def __init__(self, model, sql_repo):
        self.model = model
        self.sql_repo = sql_repo

    def embed_documents(self):
        new_docs = self.sql_repo.get_new_documents()
        sentences = []
        for pdf_path in PDF_DIR.glob('*.pdf'):
            if pdf_path.name in new_docs:
                logger.info(f'[EMBEDDER] new embedding doc: {pdf_path.name}')
                try:
                    new_sentences = self.extract_pages_with_metadata(pdf_path)
                except Exception as e:
                    logger.error(f'[EMBEDDER]: {pdf_path.name}, {e}')
                else:
                    sentences.extend(new_sentences)
        vectors = self.encode([sentence.text for sentence in sentences])
        self.sql_repo.add_bulk(sentences, vectors)
        self.sql_repo.add_bulk_documents(new_docs)

    def encode(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True)

    def extract_pages_with_metadata(self, pdf_path: Path) -> list[Sentence]:
        sentences = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue
                cleaned_text = self.text_cleaning(text)
                for chunk in self.split_text(cleaned_text):
                    sentence = Sentence(text=chunk,
                                        source=pdf_path.name,
                                        page_number=i)
                    sentences.append(sentence)
        return sentences

    def split_text(self, text: str,
                   chunk_size: int = CHUNK_SIZE,
                   overlap: int = OVERLAP) -> list[str]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk = ' '.join(words[start:end])
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks

    def text_cleaning(self, text: str) -> str:
        """ remove newlines, too many whitespaces """
        # remove header and footer
        t0 = text.replace('\n', ' ')
        t1 = ' '.join(t0.split())
        return t1
