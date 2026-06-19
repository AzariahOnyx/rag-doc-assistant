# RAG Doc Assistant — Contentstack Personalize

A Retrieval-Augmented Generation (RAG) assistant built over Contentstack Personalize documentation.

## What it does

- Chunks and embeds Contentstack Personalize docs into a ChromaDB vector store
- Uses semantic search to retrieve relevant context for any question
- Passes retrieved context to Llama 3.3 (via Groq) to generate grounded answers
- Refuses to hallucinate — if the answer isn't in the docs, it says so

## Stack

| Layer | Tool |
|---|---|
| Embeddings | ChromaDB default (all-MiniLM-L6-v2 via ONNX) |
| Vector Store | ChromaDB (in-memory) |
| LLM | Llama 3.3 70B via Groq API |
| UI | Gradio ChatInterface |
| Hosting | Hugging Face Spaces |

## Run locally

```bash
pip install chromadb groq gradio
export GROQ_API_KEY=your_key_here
python app.py
```

## Files

- `app.py` — main application (Gradio + RAG pipeline)
- `rag_personalize_v3.ipynb` — Colab notebook (development version)
- `requirements.txt` — dependencies

## Built by

Azariah Onyx — Information Architect transitioning to Gen AI.  
[LinkedIn](https://linkedin.com/in/onyx-aj)
