from sqlalchemy import create_engine

# project imports
from mars.data.tables import Base


def db_init():
    engine = create_engine('sqlite:///sentence.db')
    Base.metadata.create_all(engine)
    return engine
