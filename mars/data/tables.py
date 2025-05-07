from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class EmbeddedDocument(Base):
    __tablename__ = 'embedded_document'

    key: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class Sentence(Base):
    __tablename__ = 'sentence'

    faiss_index: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    text: Mapped[str] = mapped_column()
    source: Mapped[str] = mapped_column()
    page_number: Mapped[int] = mapped_column()


class Evaluation(Base):
    __tablename__ = 'evaluation'

    username: Mapped[str] = mapped_column()
    doc_name: Mapped[str] = mapped_column()
    complete: bool = mapped_column()
    irrelevant: bool = mapped_column()
