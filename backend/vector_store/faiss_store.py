import faiss
import os
import numpy as np
import uuid

FAISS_INDEX_PATH = "vector_store/index.faiss"

def create_or_load_index(dim: int):
    if os.path.exists(FAISS_INDEX_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
    else:
        quantizer = faiss.IndexFlatL2(dim)
        index = faiss.IndexIDMap(quantizer) 
    return index

def save_index(index):
    faiss.write_index(index, FAISS_INDEX_PATH)

def add_to_index(embeddings: list[list[float]]) -> list[str]:
    index = create_or_load_index(len(embeddings[0]))
    ids = [str(uuid.uuid4()) for _ in embeddings]
    id_array = np.array([int(uuid.UUID(i).int >> 64) for i in ids]).astype("int64")

    index.add_with_ids(np.array(embeddings).astype("float32"), id_array)
    save_index(index)
    return ids
