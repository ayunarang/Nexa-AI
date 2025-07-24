import faiss
import numpy as np
import uuid
from typing import List

def get_faiss_index(dimension: int) -> faiss.IndexIDMap:
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIDMap(quantizer)
    return index

def add_to_index(index: faiss.IndexIDMap, embeddings: List[List[float]]) -> List[str]:
    if not embeddings:
        raise ValueError("Empty embeddings list.")

    # Validate that all embeddings have the same length
    embedding_len = len(embeddings[0])
    for i, emb in enumerate(embeddings):
        if len(emb) != embedding_len:
            print([len(e) for e in embeddings])
            raise ValueError(f"Inconsistent embedding length at index {i}: got {len(emb)}, expected {embedding_len}")

    # Convert embeddings to np.float32
    embeddings_np = np.array(embeddings, dtype=np.float32)

    # Sanity check: FAISS index and embedding dim must match
    if index.d != embedding_len:
        raise ValueError(f"FAISS index dimension {index.d} does not match embedding dimension {embedding_len}")

    # Generate unique IDs
    ids = [str(uuid.uuid4()) for _ in embeddings]
    id_array = np.array([uuid.UUID(i).int & ((1 << 63) - 1) for i in ids], dtype="int64")

    # Add to FAISS
    index.add_with_ids(embeddings_np, id_array)
    return ids
