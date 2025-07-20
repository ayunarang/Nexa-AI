from sentence_transformers import SentenceTransformer

_model = None

def embed_texts(texts: list[str]) -> list[list[float]]:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model.encode(texts, show_progress_bar=False).tolist()
