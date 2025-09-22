🔹 Step 1: Install Dependencies
# Create a venv (recommended)
python3 -m venv rag_env
source rag_env/bin/activate

# Install deps
```
pip install chromadb sentence-transformers langchain ollama
```
🔹 Step 2: Run a Local LLM

Install Ollama
 then pull a model:
```
ollama pull mistral
```

Test it:

ollama run mistral "Hello"

🔹 Step 3: Prepare Your Knowledge Base

Put your FreeWays ISI info into a text file, e.g. freeways.txt:


🔹 Step 4: Python RAG Script

Here’s a minimal working example:
```python
import chromadb
from sentence_transformers import SentenceTransformer
import subprocess

# --- 1. Load embeddings model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# --- 2. Create a ChromaDB client
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("freeways")

# --- 3. Load your knowledge file
with open("freeways.txt", "r") as f:
    text = f.read()

# Split into chunks (optional)
chunks = text.split(". ")

# Add chunks to vector DB
for i, chunk in enumerate(chunks):
    if chunk.strip():
        embedding = embedder.encode(chunk).tolist()
        collection.add(documents=[chunk], embeddings=[embedding], ids=[str(i)])

# --- 4. Function to query RAG
def rag_query(query):
    q_emb = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[q_emb], n_results=3)
    context = " ".join(results["documents"][0])
    
    # Send to Ollama with retrieved context
    prompt = f"Answer the following question using this context:\n{context}\n\nQuestion: {query}"
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()

# --- 5. Try it
print(rag_query("What is FreeWays ISI?"))
print(rag_query("What activities does FreeWays organize?"))
```
🔹 Step 5: Ask Questions

Now you can query:
```
python rag_script.py
```

