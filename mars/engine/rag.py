import numpy as np
from fastapi.logger import logger
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

# project imports
from mars.core import conf
from mars.schema.rag import RagDocument
from mars.db.tables import Sentence
from mars.db.sql_repo import SqlRepository


class RAG:
    def __init__(self,
                 st_model: SentenceTransformer,
                 sql_repo: SqlRepository) -> None:
        self.st_model = st_model
        self.sql_repo = sql_repo
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=conf.CHUNK_SIZE,
            chunk_overlap=conf.OVERLAP,
            separators=conf.SEPARATORS,
            length_function=lambda s: len(self.st_model.encode(s))
        )
        self.embed_documents()

    def retrieve_documents(self,
                           query: str,
                           k: int = 5,
                           threshold: float = conf.L2_THRESHOLD) -> list[RagDocument]:
        query_embedding = self.st_model.encode(query, convert_to_numpy=True)
        qa = np.array([query_embedding])
        distances, indices = self.sql_repo.faiss_repo.search_index(qa, k)
        documents = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                logger.info(f'[RAG] recv doc with distance {distances[0][i]}')
                if distances[0][i] < threshold:
                    sentence = self.sql_repo.get_sentence(idx)
                    rag_doc = RagDocument(text=sentence.text,
                                          source=sentence.source,
                                          page_number=sentence.page_number,
                                          distance=distances[0][i])
                    documents.append(rag_doc)
        return documents

    def embed_documents(self):
        new_docs = self.sql_repo.get_new_documents()
        sentences = []
        for pdf_path in conf.PDF_DIR.glob('*.pdf'):
            if pdf_path.name in new_docs:
                logger.info(f'[EMBEDDER] new embedding doc: {pdf_path.name}')
                try:
                    new_sentences = self.extract_pages_with_metadata(pdf_path)
                except Exception as e:
                    logger.error(f'[EMBEDDER]: {pdf_path.name}, {e}')
                else:
                    sentences.extend(new_sentences)
        if sentences:
            vectors = self.st_model.encode([sentence.text for sentence in sentences],
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
