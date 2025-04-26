from pathlib import Path
from fastapi.logger import logger
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

# project imports
from mars.conf import PDF_DIR, CHUNK_SIZE, OVERLAP, SEPARATORS
from mars.data.tables import Sentence


class EmbeddingService:
    def __init__(self, model, sql_repo):
        self.model = model
        self.sql_repo = sql_repo
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=OVERLAP,
            separators=SEPARATORS,
            length_function=lambda s: len(self.model.encode(s))
        )

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
        if sentences:
            vectors = self.model.encode([sentence.text for sentence in sentences],
                                        convert_to_numpy=True)
            self.sql_repo.add_bulk(sentences, vectors)
            self.sql_repo.add_bulk_documents(new_docs)

    def extract_pages_with_metadata(self, pdf_path: Path) -> list[Sentence]:
        sentences = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue
                cleaned_text = self.text_cleaning(text)
                for chunk in self.splitter.split_text(cleaned_text):
                    sentence = Sentence(text=chunk,
                                        source=pdf_path.name,
                                        page_number=i)
                    sentences.append(sentence)
        return sentences

    def text_cleaning(self, text: str) -> str:
        """ remove newlines, too many whitespaces """
        # remove header and footer
        t0 = text.replace('\n', ' ')
        t1 = ' '.join(t0.split())
        return t1
