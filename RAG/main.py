# main.py
from RAG.config import Config
from RAG.vectorstore import VectorDB
from RAG.rag import RAG
import os

if __name__ == "__main__":
    config = Config()

    if not os.path.exists(config.faiss_index_file):
        print("Building FAISS index...")
        vectordb = VectorDB(config)
        vectordb.preprocess_file()
        vectordb.build_index()

    rag = RAG(config)

    while True:
        query = input("\nAsk Freeways chatbot: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer = rag.pipeline(query)
        print("\n🤖 Chatbot:", answer)
