# main.py
import os
from src import config
from src.data_loader import load_and_chunk_codebase
from src.vector_store import build_vector_store
from src.retriever import generate_answer_with_logging # <-- IMPORT THE NEW FUNCTION

def run_ingestion():
    """Runs the full data ingestion and vectorization pipeline."""
    print("--- Running Ingestion Pipeline ---")
    documents = load_and_chunk_codebase(config.CODEBASE_ROOT)
    if documents:
        build_vector_store(documents)
    print("--- Ingestion Complete ---")

def main():
    """Main function to run the RAG application."""
    db_exists = os.path.exists(config.CHROMA_DB_PATH) and os.listdir(config.CHROMA_DB_PATH)

    if db_exists:
        print("Existing vector database found.")
        while True:
            choice = input("Do you want to (r)e-ingest the codebase or (q)uery the existing data? [r/q]: ").lower()
            if choice in ['r', 'q']:
                break
            print("Invalid choice. Please enter 'r' or 'q'.")
        
        if choice == 'r':
            run_ingestion()
    else:
        print("No existing database found. Starting the ingestion process.")
        run_ingestion()
        
    print("\n--- Starting Interactive Query Session ---")
    print("Enter 'exit' to end the session.")
    
    try:
        while True:
            question = input("\nAsk a question about the codebase: ")
            if question.lower() == 'exit':
                print("Exiting query session. Goodbye!")
                break
            if not question.strip():
                continue
            
            # Call our new logging and answering function
            generate_answer_with_logging(question)

    except Exception as e:
        print(f"\nAn error occurred during the query session: {e}")

if __name__ == "__main__":
    main()