from fastapi.logger import logger
from sqlalchemy import select
import numpy as np

# project imports
from mars.conf import PDF_DIR
from mars.data.tables import EmbeddedDocument, Sentence


class SqlRepository:
    def __init__(self, session_factory, faiss_repo):
        self.session_factory = session_factory
        self.faiss_repo = faiss_repo

    def get_new_documents(self):
        stmt = select(EmbeddedDocument.name)
        with self.session_factory() as session:
            embedded_docs = session.scalars(stmt).all()
        doc_names = [doc.name for doc in PDF_DIR.glob('*.pdf')]
        return [doc_name for doc_name in doc_names if doc_name not in embedded_docs]

    def get_sentence(self, faiss_index: np.int64) -> Sentence:
        stmt = (select(Sentence.text,
                       Sentence.source,
                       Sentence.page_number)
                .where(Sentence.faiss_index == int(faiss_index)))
        with self.session_factory() as session:
            result = session.execute(stmt).one()
        return result

    def get_sentences(self, fids: list[np.int64]) -> list[Sentence]:
        ids = [int(fi) for fi in fids]
        stmt = (select(Sentence.text,
                       Sentence.source,
                       Sentence.page_number)
                .where(Sentence.faiss_index.in_(ids)))
        with self.session_factory() as session:
            result = session.execute(stmt).one()
        return result

    def add_embedded_document(self, name: str) -> None:
        with self.session_factory() as session:
            session.add(EmbeddedDocument(name=name))
            session.commit()

    def add_bulk_documents(self, names: list[str]) -> None:
        rows = [EmbeddedDocument(name=name) for name in names]
        with self.session_factory() as session:
            session.add_all(rows)
            session.commit()

    def add_bulk(self, sentences: list[Sentence], vecs: np.ndarray) -> None:
        ids = self.faiss_repo.add_vectors(vecs)

        for sentence, fi in zip(sentences, ids):
            sentence.faiss_index = int(fi)
        with self.session_factory() as session:
            session.add_all(sentences)
            session.commit()
