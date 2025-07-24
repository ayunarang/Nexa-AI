import numpy as np
from vector_store.embedder import embed_texts
from session_store import get_session_index, get_session_metadata
from difflib import SequenceMatcher


def keyword_match_score(query: str, text: str) -> float:
    return SequenceMatcher(None, query.lower(), text.lower()).ratio()


def normalize_scores(scores):
    min_score = float(min(scores))
    max_score = float(max(scores))
    if max_score - min_score < 1e-8:
        return [50.0 for _ in scores]
    return [
        round(100 * (score - min_score) / (max_score - min_score + 1e-8), 1)
        for score in scores
    ]


def search_chunks(
    session_id: str,
    video_id: str,
    query: str,
    top_k: int = 2,
    min_score_threshold: float = 50.0,  
    semantic_weight: float = 0.7,
    keyword_weight: float = 0.3
):
    index = get_session_index(session_id)
    metadata = get_session_metadata(session_id)

    if video_id not in metadata:
        raise ValueError("Video not found in session metadata.")

    query_vector = np.array(embed_texts([query], is_query=True)[0], dtype="float32").reshape(1, -1)

    max_fetch = max(top_k * 3, 15)
    semantic_scores, ids = index.search(query_vector, max_fetch)
    semantic_scores = semantic_scores[0]
    ids = ids[0]
    
    print("\n--- Search Results ---")
    print("Raw Semantic Scores:", semantic_scores)
    print("IDs Returned:", ids)

    id_map = {
        int(chunk["id"].replace("-", ""), 16) & ((1 << 63) - 1): chunk
        for chunk in metadata[video_id]
    }

    norm_semantic_scores = normalize_scores(semantic_scores)
    print("Normalized Semantic Scores:", norm_semantic_scores)
    
    results = []
    for idx, (raw_score, norm_score, raw_id) in enumerate(zip(semantic_scores, norm_semantic_scores, ids)):
        print(f"\nProcessing Chunk #{idx}")
        print(f"→ Raw Score: {raw_score}")
        print(f"→ Normalized Score: {norm_score}")
        print(f"→ Raw ID: {raw_id}")

        if norm_score < min_score_threshold:  
            continue

        chunk = id_map.get(raw_id)
        if not chunk:
            continue

        print(f"✓ Chunk Text: {chunk['text'][:80]}...")

        keyword_score = keyword_match_score(query, chunk["text"]) * 100
        exact_match_boost = 20 if query.lower() in chunk["text"].lower() else 0

        print(f"→ Keyword Score: {keyword_score:.2f}")
        print(f"→ Exact Match Boost: {exact_match_boost}")

        final_score = round(
            semantic_weight * norm_score + keyword_weight * keyword_score + exact_match_boost, 1
        )

        print(f"Final Combined Score: {final_score}")

        results.append({
            "id": chunk["id"],
            "start": chunk["start"],
            "end": chunk["end"],
            "text": chunk["text"],
            "score": final_score
        })

    results.sort(key=lambda r: r["score"], reverse=True)

    print("\n--- Final Top Chunks ---")
    for i, r in enumerate(results[:top_k]):
        print(f"{i+1}. Score: {r['score']} | Text: {r['text'][:80]}...")

    return results[:top_k]
