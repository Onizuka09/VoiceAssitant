# src/vectorstore.py
import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer

class VectorDB:
    def __init__(self, config):
        self.config = config
        self.model = SentenceTransformer(config.embedding_model)
        self.index = None
        self.chunks = []

    def preprocess_file(self, chunk_size=200):
        with open(self.config.data_file, "r", encoding="utf-8") as f:
            text = f.read()
        # Simple chunking by sentence length
        words = text.split()
        self.chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        return self.chunks

    def build_index(self):
        embeddings = self.model.encode(self.chunks)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        # Save index
        faiss.write_index(self.index, self.config.faiss_index_file)
        # Save chunks for retrieval
        with open(self.config.faiss_index_file + ".pkl", "wb") as f:
            pickle.dump(self.chunks, f)
        return self.index
