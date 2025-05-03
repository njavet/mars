# project imports
from mars.data.conn import session_factory


def get_session():
    yield from session_factory().get_session()
