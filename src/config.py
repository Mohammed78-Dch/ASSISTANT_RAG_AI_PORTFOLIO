from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve Environment variables' values
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 150))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 30))
TOP_K = int(os.getenv("TOP_K", 10))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
MODEL = os.getenv("MODEL", "gemini-2.5-flash")
INDEX_PATH = os.getenv("INDEX_PATH", "embeddings/faiss_index.bin")
CHUNKS_PATH = os.getenv("CHUNKS_PATH", "embeddings/chunks.json")
RESUME_PATH = os.getenv("RESUME_PATH", r"data\\john.txt")  
INDEX_PATH_EMBEDDINGS = os.getenv("INDEX_PATH_EMBEDDINGS", "embeddings/chunks_embeddings.npy")
if __name__ == "__main__":
    print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")
    print(f"CHUNK_SIZE: {CHUNK_SIZE}")
    print(f"CHUNK_OVERLAP: {CHUNK_OVERLAP}")
    print(f"TOP_K: {TOP_K}")
    print(f"EMBEDDING_MODEL: {EMBEDDING_MODEL}")
    print(f"MODEL: {MODEL}")
    print(f"INDEX_PATH: {INDEX_PATH}")
    print(f"CHUNKS_PATH: {CHUNKS_PATH}")
    print(f"RESUME_PATH: {RESUME_PATH}")
    print(f"INDEX_PATH_EMBEDDINGS: {INDEX_PATH_EMBEDDINGS}")
