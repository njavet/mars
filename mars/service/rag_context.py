# project imports
from mars.service.rag import RAG


class AppContext:
    rag: RAG | None = None

app_context = AppContext()
