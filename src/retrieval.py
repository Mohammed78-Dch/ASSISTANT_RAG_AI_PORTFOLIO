import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL, INDEX_PATH, CHUNKS_PATH, TOP_K

# Global resources (lazy-loaded and resetable)
_model = None
_index = None
_chunks = None
_current_file_hash = None
_resources_loaded = False


def _load_resources(force_reload: bool = False):
    """
    Lazy-load the model, FAISS index, and chunks.
    
    Args:
        force_reload (bool): If True, force reload all resources even if already loaded.
                            Used when a new file is uploaded.
    """
    global _model, _index, _chunks, _resources_loaded, _current_file_hash

    # If force reload, clear everything first
    if force_reload:
        print("🔄 Force reloading resources for new file...")
        unload_resources()
    
    # Load embedding model (only once, reused across files)
    if _model is None:
        print(f"📦 Loading embedding model '{EMBEDDING_MODEL}'...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        print("✅ Model loaded.")

    # Load FAISS index (file-specific)
    if _index is None or force_reload:
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(f"❌ FAISS index not found at {INDEX_PATH}")
        
        print(f"📊 Loading FAISS index from {INDEX_PATH}...")
        _index = faiss.read_index(INDEX_PATH)
        print(f"✅ FAISS index loaded ({_index.ntotal} vectors).")

    # Load chunks (file-specific)
    if _chunks is None or force_reload:
        if not os.path.exists(CHUNKS_PATH):
            raise FileNotFoundError(f"❌ Chunks file not found at {CHUNKS_PATH}")
        
        print(f"📄 Loading chunks from {CHUNKS_PATH}...")
        with open(CHUNKS_PATH, 'r', encoding='utf-8') as f:
            _chunks = json.load(f)
        print(f"✅ Loaded {len(_chunks)} chunks.")

    # Validate consistency
    if _index.ntotal != len(_chunks):
        print(f"⚠️  WARNING: Index has {_index.ntotal} vectors but {len(_chunks)} chunks loaded!")
    else:
        print(f"✅ Index and chunks are consistent ({_index.ntotal} items)")

    # Calculate file hash for tracking
    _current_file_hash = _calculate_index_hash()
    _resources_loaded = True
    
    print(f"✅ All resources loaded successfully")


def unload_resources():
    """
    Unload all resources to free memory and prepare for new file.
    This is called when a new file is uploaded to ensure clean state.
    """
    global _index, _chunks, _current_file_hash, _resources_loaded
    
    print("🧹 Unloading current resources...")
    
    # Keep the model (it's file-agnostic), but clear file-specific data
    _index = None
    _chunks = None
    _current_file_hash = None
    _resources_loaded = False
    
    print("✅ Resources unloaded (model retained for reuse)")


def reset_for_new_file():
    """
    Reset retrieval system for a new file upload.
    Clears cached index and chunks, forces reload on next retrieval.
    """
    global _index, _chunks, _current_file_hash, _resources_loaded
    
    print("\n" + "="*60)
    print("🔄 RESETTING RETRIEVAL SYSTEM FOR NEW FILE")
    print("="*60)
    
    unload_resources()
    
    print("✅ Retrieval system reset complete")
    print("   Next query will load the new file's data")
    print("="*60 + "\n")


def _calculate_index_hash() -> str:
    """Calculate hash of current index for change detection"""
    if _index is None:
        return None
    return f"{_index.ntotal}_{id(_index)}"


def retrieve(query: str, k: int = TOP_K) -> list[tuple[str, float]]:
    """
    Retrieve the top-k most relevant chunks for a query using cosine similarity.
    Returns a list of (chunk_text, similarity_score) tuples.
    
    Automatically loads resources if not already loaded.
    
    Args:
        query (str): The search query
        k (int): Number of top results to return
        
    Returns:
        list[tuple[str, float]]: List of (chunk_text, similarity_score) tuples
    """
    # Ensure resources are loaded
    if not _resources_loaded:
        print("📥 Resources not loaded, loading now...")
        _load_resources()

    # Compute query embedding
    query_embedding = np.array(_model.encode([query])).astype('float32')
    faiss.normalize_L2(query_embedding)  # normalize for cosine similarity

    # Search in FAISS (inner product on normalized vectors = cosine similarity)
    distances, indices = _index.search(query_embedding, k)

    results = []
    for i, idx in enumerate(indices[0]):
        if 0 <= idx < len(_chunks):
            similarity_score = float(distances[0][i])
            results.append((_chunks[idx], similarity_score))
        else:
            print(f"⚠️  Warning: Index {idx} is out of bounds (max: {len(_chunks)-1})")

    print(f"🔍 Retrieved {len(results)} chunks (similarity scores: {[f'{s:.3f}' for _, s in results[:3]]}...)")
    
    return results


def get_retrieval_stats() -> dict:
    """
    Get statistics about the current retrieval system state.
    
    Returns:
        dict: Statistics including loaded status, vector count, chunk count
    """
    stats = {
        "resources_loaded": _resources_loaded,
        "model_loaded": _model is not None,
        "index_loaded": _index is not None,
        "chunks_loaded": _chunks is not None,
        "vector_count": _index.ntotal if _index else 0,
        "chunk_count": len(_chunks) if _chunks else 0,
        "file_hash": _current_file_hash,
        "consistent": (_index.ntotal == len(_chunks)) if (_index and _chunks) else None
    }
    return stats


def reload_resources():
    """
    Force reload all resources from disk.
    Useful when files have been updated externally.
    """
    print("🔄 Force reloading all resources...")
    _load_resources(force_reload=True)


def is_resources_loaded() -> bool:
    """
    Check if resources are currently loaded.
    
    Returns:
        bool: True if resources are loaded and ready
    """
    return _resources_loaded and _model is not None and _index is not None and _chunks is not None


# Initialization helper
def ensure_resources_loaded():
    """
    Ensure resources are loaded. If not, load them.
    Safe to call multiple times.
    """
    if not is_resources_loaded():
        _load_resources()