# src/config.py
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = "mistral-small"
        self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        self.data_file = "freeways.txt"
        self.faiss_index_file = "RAG/freeways.index"
