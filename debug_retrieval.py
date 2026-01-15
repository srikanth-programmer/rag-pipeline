import os
import sys

# Add the project root to the python path
sys.path.append(os.getcwd())

from src.retriever import get_retriever, create_rag_chain

def debug_retrieval(question):
    print(f"Debugging retrieval for question: '{question}'")
    
    try:
        retriever = get_retriever()
        
        # 1. Check retrieved documents directly
        print("\n--- Retrieved Documents ---")
        docs = retriever.invoke(question)
        if not docs:
            print("WARNING: No documents retrieved!")
        else:
            for i, doc in enumerate(docs):
                print(f"\n[Doc {i+1}] Source: {doc.metadata.get('source', 'N/A')}")
                print(f"Content Preview: {doc.page_content[:200]}...")
        
        # 2. Check RAG Chain Answer
        print("\n--- RAG Chain Answer ---")
        rag_chain = create_rag_chain(retriever)
        response = rag_chain.invoke(question)
        print(response)
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    # Ask a question that should definitely have an answer in the codebase
    # Based on the file list, it seems to be a RAG pipeline itself.
    question = "How is the vector store built?" 
    debug_retrieval(question)
