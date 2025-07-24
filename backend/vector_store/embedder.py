import requests
from typing import List
import os

HF_API_URL = "https://api-inference.huggingface.co/models/BAAI/bge-base-en-v1.5"
HF_API_TOKEN = os.environ.get("HF_API_TOKEN") 

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

EXPECTED_DIM = 768  

def embed_texts(texts: List[str], batch_size: int = 16) -> List[List[float]]:
    embeddings: List[List[float]] = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i: i + batch_size]
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
