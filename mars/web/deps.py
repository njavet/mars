from sqlalchemy.orm import Session

# project imports
from mars.service.rag_context import app_context


def get_db_session() -> Session:
    if app_context.session_factory is None:
        raise RuntimeError('SessionFactory not initialized')
    return app_context.session_factory.get_session()
