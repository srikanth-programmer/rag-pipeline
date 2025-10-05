# src/data_loader.py
import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain_community.document_loaders import TextLoader
from langchain.docstore.document import Document

# Define the file extensions we want to process and their corresponding languages
SUPPORTED_EXTENSIONS = {
    ".py": Language.PYTHON,
    ".md": Language.MARKDOWN,
    ".js": Language.JS,
    ".ts": Language.TS,
    ".java": Language.JAVA,
    ".go": Language.GO,
    # ".yaml": Language.YAML,
    # ".json": Language.JSON,
}

def load_and_chunk_codebase(directory_path: str) -> List[Document]:
    """
    Scans a directory, processes supported files, and chunks their content.

    Args:
        directory_path: The path to the codebase directory.

    Returns:
        A list of all text chunks (as LangChain Documents) from the codebase.
    """
    all_chunks = []
    
    print(f"Starting ingestion of codebase at: {directory_path}")

    for root, _, files in os.walk(directory_path):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file)
                try:
                    print(f"-> Processing file: {file_path}")
                    loader = TextLoader(file_path, encoding="utf-8")
                    documents = loader.load()

                    language = SUPPORTED_EXTENSIONS[ext]
                    text_splitter = RecursiveCharacterTextSplitter.from_language(
                        language=language, chunk_size=1000, chunk_overlap=100
                    )

                    chunks = text_splitter.split_documents(documents)
                    
                    for chunk in chunks:
                        chunk.metadata['source'] = file_path # Add source metadata

                    all_chunks.extend(chunks)
                    print(f"   ...found {len(chunks)} chunks.")

                except Exception as e:
                    print(f"   !!! Error processing file {file_path}: {e}")

    print(f"\nTotal chunks generated across all files: {len(all_chunks)}")
    return all_chunks