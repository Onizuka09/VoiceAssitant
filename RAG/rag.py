# src/rag.py
import faiss
import pickle
from mistralai import Mistral

class RAG:
    def __init__(self, config):
        self.config = config
        self.system_prompt = "You are a helpful assistant for Freeways club members."
        self.client = Mistral(api_key=config.api_key)
        self.index = faiss.read_index(config.faiss_index_file)
        with open(config.faiss_index_file + ".pkl", "rb") as f:
            self.chunks = pickle.load(f)

    def retrieve(self, query, k=3):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(self.config.embedding_model)
        query_emb = model.encode([query])
        D, I = self.index.search(query_emb, k)
        return [self.chunks[i] for i in I[0]]

    def generate_answer(self, prompt, query, relevant_chunks):
        context = "\n".join(relevant_chunks)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"{prompt}\n\nContext:\n{context}\n\nQuestion: {query}"}
        ]
        response = self.client.chat.complete(
            model=self.config.model,
            messages=messages
        )
        return response.choices[0].message.content

    def pipeline(self, query, prompt="Answer the following question based on context, and give a minimal answer (the shortest possible):"):
        chunks = self.retrieve(query)
        return self.generate_answer(prompt, query, chunks)
