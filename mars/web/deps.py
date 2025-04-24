# project imports
from mars.data.conn import SessionFactory


session_factory  = SessionFactory()


def get_db():
    return session_factory.get_session()
