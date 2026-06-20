# RAG Doc Assistant

A RAG pipeline built over API documentation — testing how documentation structure affects AI retrieval quality.

## Live Demo

Try it now: [huggingface.co/spaces/Onyx-aj/rag-doc-assistant](https://huggingface.co/spaces/Onyx-aj/rag-doc-assistant)

## What it does

- Chunks and embeds API documentation into a vector store
- Uses semantic search to retrieve relevant context for any question
- Passes retrieved context to Llama 3.3 (via Groq) to generate grounded answers
- Refuses to hallucinate — if the answer is not in the docs, it says so

## The core insight

Poorly structured documentation degrades RAG output quality. This project tests that thesis directly — the same model, same retrieval logic, different doc structure = different answers.

Docs written for humans to scan are not the same as docs written for machines to retrieve.

## Stack

| Layer | Tool |
|---|---|
| Retrieval | Keyword search (query-optimized chunks) |
| LLM | Llama 3.3 70B via Groq API |
| UI | Gradio ChatInterface |
| Hosting | Hugging Face Spaces |

## Run locally

```bash
pip install groq gradio
export GROQ_API_KEY=your_key_here
python app.py
```

## Built by

Azariah Onyx — Information Architect transitioning to Gen AI.
[LinkedIn](https://linkedin.com/in/onyx-aj) | [Portfolio](https://azariahonyx.github.io)

