import requests
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_URL = "https://api-inference.huggingface.co/models/intfloat/e5-large-v2"
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

EXPECTED_DIM = 1024  # e5-large-v2 output dim

def embed_texts(texts: List[str], batch_size: int = 16, is_query: bool = False) -> List[List[float]]:
    """
    Embed input texts using intfloat/e5-large-v2.
    If `is_query` is True, inputs are treated as search queries (with 'query: ' prefix),
    else treated as passages/documents (with 'passage: ' prefix).
    """
    prefix = "query: " if is_query else "passage: "
    prefixed_texts = [prefix + text for text in texts]

    embeddings: List[List[float]] = []

    for i in range(0, len(prefixed_texts), batch_size):
        batch = prefixed_texts[i: i + batch_size]
        response = requests.post(HF_API_URL, headers=headers, json={"inputs": batch})

        if response.status_code != 200:
            raise RuntimeError(f"HF API error {response.status_code}: {response.text}")

        result = response.json()

        if isinstance(result[0], float):
            result = [result]

        for j, emb in enumerate(result):
            if len(emb) != EXPECTED_DIM:
                raise ValueError(f"Embedding at index {i + j} has invalid dimension: {len(emb)}")
            embeddings.append(emb)

    return embeddings
