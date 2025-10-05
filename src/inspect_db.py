# inspect_db.py

import chromadb
import config

def inspect_vector_store():
    """
    Connects to the existing ChromaDB and prints its contents for inspection.
    """
    print(f"--- Inspecting Vector Store at: {config.CHROMA_DB_PATH} ---")
    
    try:
        # 1. Initialize a persistent ChromaDB client
        client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        
        # 2. Get the specific collection
        collection = client.get_collection(name=config.CHROMA_COLLECTION_NAME)
        
        # 3. Get the total number of items
        count = collection.count()
        if count == 0:
            print("The database is empty.")
            return
        
        print(f"Found {count} items in the collection '{config.CHROMA_COLLECTION_NAME}'.")
        
        # 4. Ask the user how many items to display
        while True:
            try:
                limit_str = input(f"How many items would you like to view? (Enter a number, or 'all'): ")
                if limit_str.lower() == 'all':
                    limit = count
                    break
                limit = int(limit_str)
                break
            except ValueError:
                print("Invalid input. Please enter a number or 'all'.")

        # 5. Retrieve the items from the collection
        # We ask for the documents (the text chunks) and their metadata.
        # We don't need to see the actual embeddings (the long list of numbers).
        results = collection.get(
            limit=limit,
            include=["metadatas", "documents"]
        )
        
        # 6. Print the results in a readable format
        for i in range(len(results['ids'])):
            doc_id = results['ids'][i]
            metadata = results['metadatas'][i]
            document_content = results['documents'][i]
            
            print("\n" + "="*50)
            print(f"Item ID: {doc_id}")
            print(f"Source File: {metadata.get('source', 'N/A')}")
            print("-" * 50)
            print("Content (Chunk):")
            print(document_content)
            print("="*50)
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure the database exists and the collection name is correct.")

if __name__ == "__main__":
    inspect_vector_store()