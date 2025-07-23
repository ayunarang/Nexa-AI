import requests
from typing import List

EMBEDDER_URL = "https://embedder-service.onrender.com/embed"  

def embed_texts(texts: List[str]) -> List[List[float]]:
    try:
        response = requests.post(EMBEDDER_URL, json={"texts": texts})
        response.raise_for_status()
        return response.json()["embeddings"]
    except Exception as e:
        print("Error embedding text:", str(e))
        return []
