from rich.console import Console
from sqlalchemy import select, in_
import numpy as np

# project imports
from mars.data.tables import EmbeddedDocument, Sentence


class SqlRepository:
    def __init__(self, session, faiss_repo):
        self.console = Console()
        self.session = session
        self.faiss_repo = faiss_repo

    def get_embedded_documents(self):
        stmt = select(EmbeddedDocument.name)
        return self.session.scalars(stmt).all()

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

    def add_bulk(self,
                 chunks: list[str],
                 sources: list[str],
                 pages: list[int],
                 vecs: np.ndarray) -> None:
        ids = self.faiss_repo.add_vectors(vecs)

        rows = [Sentence(faiss_index=int(fi),
                         text=c,
                         source=s,
                         page_number=p)
                for fi, c, s, p in zip(ids, chunks, sources, pages)]
        self.session.add_all(rows)
        self.session.commit()
