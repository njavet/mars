import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import faiss
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import DB_URL, SENTENCE_TRANSFORMER_NAME
from mars.utils.text_helpers import extract_pdfs
from mars.data.repo import Repository
from mars.data.tables import Base


def db_init():
    # init sqlalchemy
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)

    if not os.path.exists('index.faiss'):
        print('creating faiss index...')
        # create faiss index
        model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
        dimension = model.get_sentence_embedding_dimension()
        index = faiss.IndexFlatL2(dimension)
        faiss.write_index(index, 'index.faiss')

        # embed pdfs
        with Session(engine) as session:
            repo = Repository(session)
            embed_documents(model, repo)


def embed_documents(model, repo):
    sentences = extract_pdfs()
    for idx, sentence in enumerate(sentences):
        embedding = model.encode(sentence.text)
        repo.add_embedding(embedding)
        sentence.faiss_index = idx
    repo.save_faiss_index()
    repo.save_sentences(sentences)
