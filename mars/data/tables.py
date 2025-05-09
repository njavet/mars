from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import (DeclarativeBase,
                            mapped_column,
                            Mapped,
                            relationship)


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


class EvalDocTable(Base):
    __tablename__ = 'eval_doc'

    server: Mapped[str] = mapped_column()
    filename: Mapped[str] = mapped_column()
    run: Mapped[int] = mapped_column()
    scores: Mapped[list['EvalScoreTable']] = relationship(back_populates='doc')


class EvalScoreTable(Base):
    __tablename__ = 'eval_score'

    key: Mapped[int] = mapped_column(primary_key=True)
    lm_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    complete: Mapped[bool] = mapped_column()
    irrelevant: Mapped[bool] = mapped_column()
    concise: Mapped[bool] = mapped_column()

    fk_doc: Mapped[int] = mapped_column(ForeignKey('eval_doc_table.key'))
    doc: Mapped['EvalDocTable'] = relationship(back_populates='scores')
