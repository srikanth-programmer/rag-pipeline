# src/vector_store.py
import time
from typing import List
from langchain.docstore.document import Document
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from src import config

def get_embedding_model():
    """Initializes and returns the Vertex AI embedding model."""
    print(f"Initializing embedding model: {config.EMBEDDING_MODEL_NAME}")
    return VertexAIEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)

def build_vector_store(chunks: List[Document]):
    """
    Embeds documents in small, delayed batches and stores them in a persistent 
    ChromaDB vector store to avoid hitting strict API rate limits.
    """
    if not chunks:
        print("No chunks to process. Exiting.")
        return

    print(f"\n--- Stage 2: Embedding and Storage ---")
    embedding_model = get_embedding_model()
    
    print(f"Initializing ChromaDB at: {config.CHROMA_DB_PATH}")
    vector_db = Chroma(
        persist_directory=config.CHROMA_DB_PATH,
        embedding_function=embedding_model,
        collection_name=config.CHROMA_COLLECTION_NAME,
    )

    # Process documents in controlled batches
    total_chunks = len(chunks)
    for i in range(0, total_chunks, config.EMBEDDING_BATCH_SIZE):
        batch = chunks[i:i + config.EMBEDDING_BATCH_SIZE]
        
        current_batch_num = (i // config.EMBEDDING_BATCH_SIZE) + 1
        # Recalculate total batches based on the new batch size
        total_batches = (total_chunks + config.EMBEDDING_BATCH_SIZE - 1) // config.EMBEDDING_BATCH_SIZE
        
        print(f"--> Processing batch {current_batch_num}/{total_batches} ({len(batch)} chunks)...")
        
        vector_db.add_documents(batch)
        
        # Add a configurable delay between batches to respect rate limits
        print(f"    ...batch added. Pausing for {config.EMBEDDING_REQUEST_DELAY_SECONDS} seconds.")
        time.sleep(config.EMBEDDING_REQUEST_DELAY_SECONDS)

    print("\nVector store built and persisted successfully.")
    print(f"Total vectors in store: {vector_db._collection.count()}")

