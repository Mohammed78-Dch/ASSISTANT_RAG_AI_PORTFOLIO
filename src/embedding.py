import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from .chunking import chunk_resume_data
from .config import RESUME_PATH, CHUNKS_PATH, INDEX_PATH, EMBEDDING_MODEL

# File Load / Save Functions
def save_chunks_to_file(chunks, chunks_file_path):
    os.makedirs(os.path.dirname(chunks_file_path), exist_ok=True)
    with open(chunks_file_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2)
    print(f"Saved {len(chunks)} chunks to {chunks_file_path}")

# Embedding & FAISS Index
def create_and_save_embeddings(chunks, index_path, chunks_path, model_name=EMBEDDING_MODEL, batch_size=32):
    if not chunks:
        print("No chunks provided to embed. Exiting.")
        return

    print(f"Loading embedding model: {model_name}...")
    model = SentenceTransformer(model_name)
    print("Model loaded.")

    print(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = model.encode(chunks, batch_size=batch_size, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    print("Embeddings normalized for cosine similarity.")

    dimension = embeddings.shape[1]
    print(f"Embedding dimension: {dimension}")

    print("Creating FAISS index...")
    index = faiss.IndexFlatIP(dimension)  # IP = inner product for cosine similarity on normalized vectors
    index.add(embeddings)
    print(f"FAISS index created with {index.ntotal} vectors.")

    # Save FAISS index
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)
    print(f"FAISS index saved to {index_path}")

    # Save chunks
    save_chunks_to_file(chunks, chunks_path)

    # Save embeddings as .npy for future use
    embeddings_file = os.path.splitext(chunks_path)[0] + "_embeddings.npy"
    np.save(embeddings_file, embeddings)
    print(f"Embeddings saved to {embeddings_file}")

    print("Embedding generation and saving complete!")

# Use Example
def main():
    if not os.path.exists(RESUME_PATH):
        print(f"Error: Raw resume file not found at {RESUME_PATH}.")
        return

    print(f"Loading raw resume text from {RESUME_PATH}...")
    with open(RESUME_PATH, 'r', encoding='utf-8') as f:
        raw_resume_text = f.read()
    print("Raw resume text loaded.")

    print("Generating chunks using chunk_resume_data()...")
    chunks = chunk_resume_data(raw_resume_text)
    print(f"Chunking complete. Generated {len(chunks)} chunks.")

    print("Creating embeddings and saving FAISS index...")
    create_and_save_embeddings(chunks, INDEX_PATH, CHUNKS_PATH)

if __name__ == "__main__":
    main()
