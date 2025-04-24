# project imports
from mars.data.conn import SessionFactory


session_factory  = SessionFactory()


def get_db():
    with session_factory.get_session() as session:
        yield session
