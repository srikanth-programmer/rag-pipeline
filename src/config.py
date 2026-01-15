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
CODEBASE_ROOT = "/home/srikanth/Work/Angular/angular-tailwind/" 
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

# --- Authentication ---
from google.oauth2 import service_account

SERVICE_ACCOUNT_KEY_PATH = "service-account-key.json"

def get_credentials():
    """Loads the service account credentials from the key file."""
    if os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
        return service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_KEY_PATH)
    else:
        print(f"Warning: Service account key not found at {SERVICE_ACCOUNT_KEY_PATH}. Using default credentials.")
        return None