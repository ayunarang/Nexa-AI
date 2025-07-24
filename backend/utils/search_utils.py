import numpy as np
from vector_store.embedder import embed_texts
from session_store import get_session_index, get_session_metadata
from difflib import SequenceMatcher

def keyword_match_score(query: str, text: str) -> float:
    return SequenceMatcher(None, query.lower(), text.lower()).ratio()

def distances_to_similarities(distances):
    similarities = 1 - distances / 2
    return np.clip(similarities, 0, 1)  

def normalize_scores(scores):
    min_score = float(min(scores))
    max_score = float(max(scores))
    denom = max_score - min_score if max_score - min_score > 1e-8 else 1e-8
    return [
        round(100 * (score - min_score) / denom, 1) 
        for score in scores
    ]

def search_chunks(session_id: str, video_id: str, query: str, top_k: int,
                  semantic_weight: float = 0.7, keyword_weight: float = 0.3):

    index = get_session_index(session_id)
    metadata = get_session_metadata(session_id)

    if video_id not in metadata:
        raise ValueError("Video not found in session metadata.")

    query_vector = np.array(embed_texts([query])[0], dtype="float32")
    query_vector /= np.linalg.norm(query_vector) + 1e-10
    query_vector = query_vector.reshape(1, -1)

    max_fetch = max(top_k * 3, 15)

    distances, ids = index.search(query_vector, max_fetch)
    distances = distances[0]
    ids = ids[0]

    similarities = distances_to_similarities(distances)

    id_map = {chunk["id"]: chunk for chunk in metadata[video_id]}

    norm_similarities = normalize_scores(similarities)

    results = []


    for sim, norm_sim, raw_id in zip(similarities, norm_similarities, ids):
        if raw_id == -1:
            continue

        chunk = id_map.get(raw_id)
        if not chunk:
            continue

        keyword_score = keyword_match_score(query, chunk["text"]) * 100
        exact_match_boost = 20 if query.lower() in chunk["text"].lower() else 0

        final_score = round(
            semantic_weight * norm_sim + keyword_weight * keyword_score + exact_match_boost, 1
        )

        results.append({
            "start": chunk["start"],
            "end": chunk["end"],
            "text": chunk["text"],
            "score": final_score
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_k]
