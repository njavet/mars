from sqlalchemy import create_engine
import faiss
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import DB_URL, SENTENCE_TRANSFORMER_NAME
from mars.data.tables import Base


def db_init():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)

    model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
    dimension = model.get_sentence_embedding_dimension()
    index = faiss.IndexFlatL2(dimension)
    faiss.write_index(index, 'index.faiss')
