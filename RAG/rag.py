import faiss
import pickle
import os
from mistralai import Mistral
from google import genai  # Requires `google-generativeai` package
from google.genai import types

from sentence_transformers import SentenceTransformer


class RAG:
    def __init__(self, config):
        self.config = config
        self.system_prompt = (
            "You are a helpful assistant for Freeways club guests. "
            "You'll be given the question transformed from speech using STT (consider transformation errors). "
            "If you detect an error do not mention it, just give the answer assuming you got a correct question."
        )

        # --- LLM Clients ---
        self.mistral_client = Mistral(api_key=config.api_key)
        self.gemini_client = genai.Client(api_key=config.gemini_api_key)

        # --- Load FAISS index & chunks ---
        self.index = faiss.read_index(config.faiss_index_file)
        with open(config.faiss_index_file + ".pkl", "rb") as f:
            self.chunks = pickle.load(f)

        # --- Embedding model (loaded once for efficiency) ---
        self.embedding_model = SentenceTransformer(self.config.embedding_model)

    def retrieve(self, query, k=3):
        query_emb = self.embedding_model.encode([query])
        D, I = self.index.search(query_emb, k)
        return [self.chunks[i] for i in I[0]]

    # ---------------- LLM CALL METHODS ---------------- #

    def call_mistral(self, messages):
        response = self.mistral_client.chat.complete(
            model=self.config.model,
            messages=messages,
            temperature=0.1,
        )
        return response.choices[0].message.content

    def call_gemini(self, messages):
        # Gemini expects text input, so convert the messages into a single prompt
        formatted_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        response = self.gemini_client.models.generate_content(
            model=self.config.gemini_model,
            contents=formatted_prompt,
            config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=1024),
        )
        return response.text

    # ---------------- RAG LOGIC ---------------- #

    def generate_answer(self, prompt, query, relevant_chunks):
        context = "\n".join(relevant_chunks)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"{prompt}\n\nContext:\n{context}\n\nQuestion: {query}"}
        ]

        if self.config.llm_provider == "mistral":
            return self.call_mistral(messages)
        elif self.config.llm_provider == "gemini":
            return self.call_gemini(messages)
        else:
            raise ValueError(f"Unknown LLM provider: {self.config.llm_provider}")

    def pipeline(
        self,
        query,
        prompt=(
            "Answer the following question based on context, "
            "and give a minimal and short answer, do not give any info out of the context, "
            "if the question is not clear just say 'I don't know' or 'can you repeat the question please'."
        ),
    ):
        chunks = self.retrieve(query)
        return self.generate_answer(prompt, query, chunks)
