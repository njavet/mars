# project imports
from mars.data.conn import SessionFactory
from mars.service.rag import RAG


class AppContext:
    rag: RAG | None = None
    session_factory: SessionFactory | None = None


app_context = AppContext()
