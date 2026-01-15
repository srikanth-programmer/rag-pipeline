import shutil
import os
import sys

# Add the project root to the python path
sys.path.append(os.getcwd())

from src import config
from src.data_loader import load_and_chunk_codebase
from src.vector_store import build_vector_store

def reingest():
    print("Starting Re-ingestion Process...")
    
    # 1. Clear existing DB to remove stale data
    if os.path.exists(config.CHROMA_DB_PATH):
        print(f"Removing existing DB at '{config.CHROMA_DB_PATH}' to ensure clean slate...")
        shutil.rmtree(config.CHROMA_DB_PATH)
    else:
        print(f"No existing DB found at '{config.CHROMA_DB_PATH}'.")
    
    # 2. Load and Chunk Documents
    # config.CODEBASE_ROOT is already set to "/home/srikanth/Work/Angular/angular-tailwind/"
    print(f"Target Codebase: {config.CODEBASE_ROOT}")
    documents = load_and_chunk_codebase(config.CODEBASE_ROOT)
    
    if not documents:
        print("ERROR: No documents found! Please check if the path exists and contains supported files.")
        return

    # 3. Build Vector Store
    build_vector_store(documents)
    print("Re-ingestion complete.")

if __name__ == "__main__":
    reingest()
