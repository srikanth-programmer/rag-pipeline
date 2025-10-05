# src/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Project Configuration ---
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

# --- Data Ingestion Configuration ---
# Path to the codebase to be ingested
CODEBASE_ROOT = "/home/srikanth/Work/testing_code_base/python-mini-project" 
# Path to the persistent ChromaDB database
CHROMA_DB_PATH = "db"
# Name of the collection within ChromaDB
CHROMA_COLLECTION_NAME = "codebase_rag"

# --- Embedding Model Configuration ---
# See a list of available models here: https://cloud.google.com/vertex-ai/docs/generative-ai/model-garden/model-versions
EMBEDDING_MODEL_NAME = "text-embedding-004"

EMBEDDING_BATCH_SIZE = 5

EMBEDDING_REQUEST_DELAY_SECONDS = 3

GENERATIVE_MODEL_NAME = "gemini-2.5-flash"