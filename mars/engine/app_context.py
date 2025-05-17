# project imports
from mars.engine.rag import RAG


class AppContext:
    rag: RAG | None = None


app_context = AppContext()
