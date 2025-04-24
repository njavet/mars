from sqlalchemy import select

# project imports
from mars.schemas import RagDocument
from mars.data.tables import Sentence


class Repository:
    def __init__(self, session):
        self.session = session

    def save_sentences(self, sentences: list[Sentence]):
        self.session.add_all(sentences)
        self.session.commit()

    def get_sentences(self):
        stmt = select(Sentence)
        results = self.session.scalars(stmt).all()
        dix = {}
        for result in results:
            dix[result.faiss_index] = RagDocument(text=result.text,
                                                  source=result.source,
                                                  page_number=result.page_number)
        return dix
