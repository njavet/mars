from sqlalchemy import create_engine

# project imports
from mars.conf import DB_URL
from mars.data.tables import Base


def db_init():
    # init sqlalchemy
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
