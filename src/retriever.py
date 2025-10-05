# src/retriever.py

import os
import re
import datetime
from langchain_google_vertexai import VertexAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src import config
from src.vector_store import get_embedding_model

def get_retriever():
    """Initializes and returns a retriever for the existing ChromaDB vector store."""
    print("Connecting to existing vector store...")
    vector_db = Chroma(
        persist_directory=config.CHROMA_DB_PATH,
        embedding_function=get_embedding_model(),
        collection_name=config.CHROMA_COLLECTION_NAME,
    )
    return vector_db.as_retriever(search_kwargs={"k": 4})

def create_rag_chain(retriever):
    """Creates the main RAG chain for question answering."""
    # This function is slightly simplified to just build the chain
    llm = VertexAI(model_name=config.GENERATIVE_MODEL_NAME, temperature=0.1)

    prompt_template = """
    You are an expert software developer assistant. Your task is to answer questions about a codebase.
    Use ONLY the following pieces of retrieved context to answer the question.
    If you don't know the answer from the context provided, just say that you don't know. 
    Do not make up an answer. Keep the answer concise and to the point.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    prompt = PromptTemplate.from_template(prompt_template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

def _sanitize_filename(text: str) -> str:
    """Helper function to create a safe filename from a question."""
    # Remove non-alphanumeric characters
    text = re.sub(r'[^\w\s-]', '', text).strip()
    # Replace spaces with underscores and limit length
    return text.replace(' ', '_')[:50]

def generate_answer_with_logging(question: str):
    """
    1. Retrieves context for a question.
    2. Logs the question and retrieved context to a file.
    3. Invokes the RAG chain to generate and stream the answer.
    """
    print(f"\n> Processing question: '{question}'...")
    
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # --- Part 1: Retrieve the context ---
    retriever = get_retriever()
    retrieved_docs = retriever.get_relevant_documents(question)
    
    # --- Part 2: Log the context to a file ---
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = _sanitize_filename(question)
    log_filename = f"logs/log_{timestamp}_{safe_filename}.txt"
    
    with open(log_filename, 'w', encoding='utf-8') as f:
        f.write(f"QUERY: {question}\n")
        f.write("="*50 + "\n")
        f.write("RETRIEVED CONTEXT:\n")
        f.write("="*50 + "\n\n")
        
        for i, doc in enumerate(retrieved_docs):
            f.write(f"--- Context Chunk {i+1} ---\n")
            f.write(f"Source: {doc.metadata.get('source', 'N/A')}\n\n")
            f.write(doc.page_content)
            f.write("\n\n")
            
    print(f"   ...Context has been saved to '{log_filename}'")
    
    # --- Part 3: Generate the answer using the full RAG chain ---
    rag_chain = create_rag_chain(retriever)
    
    print("\n--- Answer ---")
    for chunk in rag_chain.stream(question):
        print(chunk, end="", flush=True)
    print("\n\n--- End of Answer ---")