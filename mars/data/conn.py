from contextlib import contextmanager
from fastapi.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# project imports
from mars.conf import DB_URL
from mars.data.tables import Base


class SessionFactory:
    def __init__(self, db_url=DB_URL):
        logger.info(f'Creating SessionFactory singleton: {db_url}')
        self._engine = create_engine(db_url)
        Base.metadata.create_all(self._engine)
        self._sessionmaker = sessionmaker(bind=self._engine,
                                          expire_on_commit=False)

    @contextmanager
    def get_session(self):
        db = self._sessionmaker()
        try:
            yield db
        finally:
            db.close()

    def __call__(self):
        return self.get_session()
