from sqlalchemy import select
import numpy as np

# project imports
from mars.conf import PDF_DIR
from mars.data.tables import EmbeddedDocument, Sentence


class SqlRepository:
    def __init__(self, session, faiss_repo):
        self.session = session
        self.faiss_repo = faiss_repo

    def get_new_documents(self):
        stmt = select(EmbeddedDocument.name)
        embedded_docs = self.session.scalars(stmt).all()
        doc_names = [doc.name for doc in PDF_DIR.glob('*.pdf')]
        return [doc_name for doc_name in doc_names if doc_name not in embedded_docs]

    def get_sentence(self, faiss_index: np.int64) -> Sentence:
        stmt = (select(Sentence.text,
                       Sentence.source,
                       Sentence.page_number)
                .where(Sentence.faiss_index == int(faiss_index)))
        result = self.session.execute(stmt).one()
        return result

    def get_sentences(self, fids: list[np.int64]) -> list[Sentence]:
        ids = [int(fi) for fi in fids]
        stmt = (select(Sentence.text,
                       Sentence.source,
                       Sentence.page_number)
                .where(Sentence.faiss_index.in_(ids)))
        result = self.session.scalars(stmt).all()
        return result

    def add_embedded_document(self, name: str) -> None:
        self.session.add(EmbeddedDocument(name=name))
        self.session.commit()

    def add_bulk_documents(self, names: list[str]) -> None:
        rows = [EmbeddedDocument(name=name) for name in names]
        self.session.add_all(rows)
        self.session.commit()

    def add_bulk(self, sentences: list[Sentence], vecs: np.ndarray) -> None:
        ids = self.faiss_repo.add_vectors(vecs)

        for sentence, fi in zip(sentences, ids):
            sentence.faiss_index = fi
        self.session.add_all(sentences)
        self.session.commit()
