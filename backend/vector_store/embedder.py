from sentence_transformers import SentenceTransformer
from typing import List

_model = None

def embed_texts(texts: List[str], batch_size: int = 16) -> List[List[float]]:
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = _model.encode(batch, show_progress_bar=False).tolist()
        embeddings.extend(batch_embeddings)
    
    return embeddings
