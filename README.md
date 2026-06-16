# rag-doc-assistant

> A RAG pipeline built over Contentstack documentation — testing what makes documentation LLM-friendly vs AI-inhibited.

## What this is

Most RAG pipelines fail not because of the model — but because the documentation going in is AI-inhibited.

This project builds a retrieval-augmented generation (RAG) pipeline over real enterprise documentation (Contentstack) to answer two questions:

1. What makes documentation machine-readable vs AI-inhibited?
2. How do you architect docs so an LLM can retrieve and use them accurately?

## Stack

| Tool | Purpose |
|------|---------|
| LangChain | Orchestration and retrieval chain |
| ChromaDB | Vector store for doc embeddings |
| OpenAI / HuggingFace | Embeddings and LLM |
| Python | Core language |
| Contentstack Docs | Source documentation corpus |

## Project structure

```
rag-doc-assistant/
├── data/               # Raw and processed documentation chunks
├── embeddings/         # Vector store (ChromaDB)
├── pipeline/           # LangChain RAG chain setup
│   ├── ingest.py       # Load and chunk docs
│   ├── embed.py        # Generate and store embeddings
│   └── query.py        # Query the RAG pipeline
├── evaluation/         # Doc quality scoring experiments
├── notebooks/          # Experiments and findings
└── README.md
```

## The hypothesis

Documentation written for humans is often terrible for AI. Specifically:

- **Implicit context** — writers assume the reader knows the product. LLMs don't.
- **Inconsistent structure** — headings, chunking boundaries, and terminology vary wildly.
- **Cross-reference dependencies** — "see above" and "as mentioned earlier" break retrieval entirely.
- **Passive voice and nominalizations** — reduce semantic clarity for embeddings.

This project tests these hypotheses against real retrieval quality metrics.

## Status

- [x] Repo initialized
- [ ] Doc ingestion pipeline (Week 2)
- [ ] ChromaDB vector store setup (Week 2)
- [ ] RAG query pipeline (Week 2)
- [ ] Doc quality scoring framework (Week 3)
- [ ] Findings writeup + LinkedIn post (Week 3)

## Why this matters

If you're building AI products on top of documentation — support bots, internal knowledge bases, product copilots — the quality of your documentation architecture directly determines the quality of your AI outputs.

This is not an ML problem. It's a documentation problem.

## Author

**Azariah Onyx** — Information Architect → Gen AI  
[LinkedIn](https://linkedin.com/in/onyx-aj) · [GitHub](https://github.com/AzariahOnyx)
