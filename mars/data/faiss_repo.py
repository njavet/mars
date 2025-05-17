import os
import numpy as np
import faiss
from fastapi.logger import logger

# project imports
from mars.conf import FAISS_INDEX


class FaissRepository:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = self.get_faiss_index()

    def get_faiss_index(self):
        if not os.path.exists(FAISS_INDEX):
            logger.info(f'[FAISS REPO] creating faiss index {FAISS_INDEX}')
            index = faiss.IndexIDMap(faiss.IndexFlatL2(self.dim))
            faiss.write_index(index, FAISS_INDEX)
        index = faiss.read_index(FAISS_INDEX)

        if not isinstance(index, faiss.IndexIDMap):
            index = faiss.IndexIDMap(index)
        return index

    def search_index(self, query_array: np.ndarray, k: int = 5):
        distances, indices = self.index.search(query_array, k)
        return distances, indices

    def add_vectors(self, vecs: np.ndarray):
        start = self.index.ntotal
        ids = np.arange(start, start + len(vecs), dtype=np.int64)
        logger.info(f'[FAISS REPO] adding {len(vecs)} vectors, starting at {start}')
        self.index.add_with_ids(vecs, ids)
        logger.info(f'[FAISS REPO] index contains {self.index.ntotal} vectors')
        self.flush()
        return ids

    def flush(self):
        faiss.write_index(self.index, FAISS_INDEX)
