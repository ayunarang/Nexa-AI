import faiss
import numpy as np

def get_faiss_index() -> faiss.IndexIDMap:
    dim = 384  
    quantizer = faiss.IndexFlatL2(dim)
    index = faiss.IndexIDMap(quantizer)
    return index

def add_to_index(index: faiss.IndexIDMap, embeddings: list[list[float]], chunk_ids: list[int]) -> list[int]:
    assert len(embeddings) == len(chunk_ids), "Mismatch between number of vectors and IDs"
    normalized_embeddings = []
    for emb in embeddings:
        emb = np.array(emb)
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
        normalized_embeddings.append(emb)

    id_array = np.array(chunk_ids, dtype="int64")
    index.add_with_ids(np.array(normalized_embeddings).astype("float32"), id_array)
    return chunk_ids
