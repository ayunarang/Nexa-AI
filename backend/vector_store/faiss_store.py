import faiss
import numpy as np
import uuid

def get_faiss_index() -> faiss.IndexIDMap:
    dim = 384  
    quantizer = faiss.IndexFlatL2(dim)
    index = faiss.IndexIDMap(quantizer)
    return index

def add_to_index(index: faiss.IndexIDMap, embeddings: list[list[float]]) -> list[str]:
    ids = [str(uuid.uuid4()) for _ in embeddings]
    id_array = np.array([uuid.UUID(i).int & ((1 << 63) - 1) for i in ids], dtype="int64")
    index.add_with_ids(np.array(embeddings).astype("float32"), id_array)
    return ids
