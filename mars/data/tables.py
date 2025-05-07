from sqlalchemy import BigInteger, ForeignKey
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


class EvaluationDocument(Base):
    __tablename__ = 'evaluation_document'

    key: Mapped[int] = mapped_column(primary_key=True)
    server: Mapped[str] = mapped_column()
    filename: Mapped[str] = mapped_column()
    system_message: Mapped[str] = mapped_column()


class EvaluationResult(Base):
    __tablename__ = 'evaluation_result'

    key: Mapped[int] = mapped_column(primary_key=True)
    lm_name: str
    output: str

    fk_eval: Mapped[int] = mapped_column(ForeignKey(EvaluationDocument.key))


class EvaluationScore(Base):
    __tablename__ = 'evaluation_score'

    key: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    complete: Mapped[bool] = mapped_column()
    irrelevant: Mapped[bool] = mapped_column()

    fk_result: Mapped[int] = mapped_column(ForeignKey(EvaluationResult.key))
