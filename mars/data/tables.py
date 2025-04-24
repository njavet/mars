from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class Sentence(Base):
    __tablename__ = 'sentence'

    faiss_index: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    source: Mapped[str] = mapped_column()
    page_number: Mapped[int] = mapped_column()
