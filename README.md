# RAG Pipeline for Codebase Question Answering

This project implements a Retrieval-Augmented Generation (RAG) pipeline for answering questions about a codebase using Google Vertex AI and ChromaDB. It ingests source code, creates embeddings, stores them in a vector database, and enables interactive querying with context-aware answers.

## Features

- **Codebase Ingestion:** Recursively scans a codebase, splits supported files (Python, Markdown, JS, TS, Java, Go) into chunks, and adds source metadata.
- **Embeddings:** Uses Google Vertex AI's embedding model to generate vector representations of code/document chunks.
- **Vector Store:** Stores embeddings in a persistent ChromaDB database for efficient retrieval.
- **RAG Chain:** Retrieves relevant code/document chunks and uses a generative LLM (Vertex AI) to answer user questions with context.
- **Interactive CLI:** Supports re-ingestion and interactive Q&A sessions. Logs each query and its retrieved context.
- **Database Inspection:** Utility to inspect the contents of the ChromaDB vector store.

## Project Structure

```
main.py                # Entry point for ingestion and interactive Q&A
src/
  config.py            # Configuration (paths, model names, batch sizes)
  data_loader.py       # Loads and chunks codebase files
  vector_store.py      # Embeds and stores chunks in ChromaDB
  retriever.py         # Retrieves context and runs the RAG chain
  inspect_db.py        # Utility to inspect the vector store
  __init.py
logs/                  # Query logs
pyproject.toml         # Project dependencies
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or use pyproject.toml with your preferred tool (e.g., poetry, pipx)
   ```
2. **Set up environment variables:**
   - Create a `.env` file with your Google Cloud project and location:
     ```env
     GOOGLE_CLOUD_PROJECT=your-project-id
     GOOGLE_CLOUD_LOCATION=your-location
     ```
3. **Configure codebase path:**
   - Edit `src/config.py` and set `CODEBASE_ROOT` to the path of the codebase you want to ingest.

## Usage

- **Run the main pipeline:**

  ```bash
  python main.py
  ```

  - On first run, it will ingest the codebase and build the vector store.
  - On subsequent runs, you can choose to re-ingest or query the existing data.
  - Enter questions about the codebase interactively. Type `exit` to quit.

- **Inspect the vector store:**
  ```bash
  python src/inspect_db.py
  ```

## Dependencies

- Python 3.12+
- [ChromaDB](https://www.trychroma.com/)
- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai)
- [LangChain](https://python.langchain.com/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Notes

- Only files with supported extensions are ingested.
- Embedding and generative models are configurable in `src/config.py`.
- Query logs are saved in the `logs/` directory for traceability.
