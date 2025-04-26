import os
from rich.console import Console
import numpy as np
import faiss

# project imports
from mars.conf import FAISS_INDEX


class FaissRepository:
    def __init__(self, dim: int):
        self.console = Console()
        self.index = self.get_faiss_index(dim)

    def get_faiss_index(self, dim):
        if not os.path.exists(FAISS_INDEX):
            self.console.print('creating faiss index...')
            index = faiss.IndexFlatL2(dim)
            faiss.write_index(index, FAISS_INDEX)
        index = faiss.read_index(FAISS_INDEX)
        return index

    def search_index(self, query_array: np.ndarray, k: int = 5):
        distances, indices = self.index.search(query_array, k)
        return distances, indices

    def add_vectors(self, vecs: np.ndarray):
        start = self.index.ntotal
        ids = np.arange(start, start + len(vecs), dtype=np.int64)
        self.index.add_with_ids(vecs, ids)
        return ids

    def flush(self):
        faiss.write_index(self.index, FAISS_INDEX)
