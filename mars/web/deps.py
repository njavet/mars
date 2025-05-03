# project imports
from mars.service.service import init_rag


# singleton global instances
rag = init_rag()


def get_rag():
    return rag
