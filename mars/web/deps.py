from mars.data.conn import session_factory


def get_db():
    with session_factory.get_session() as session:
        yield session
