import requests
import numpy as np
import time
import random

RENDER_EMBEDDING_URL = "https://embedder-service.onrender.com/embed"
BATCH_SIZE = 10
TIMEOUT = 30
RETRIES = 3
BACKOFF_FACTOR = 2.0

def post_with_retry(url, json, timeout, retries=3, backoff_factor=2.0):
    for attempt in range(retries):
        try:
            response = requests.post(url, json=json, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt < retries - 1:
                sleep_time = backoff_factor ** attempt + random.uniform(0, 1)
                print(f"Retry {attempt+1} failed: {e}. Retrying in {sleep_time:.1f}s...")
                time.sleep(sleep_time)
            else:
                print(f"Final retry failed: {e}")
                return None

def embed_texts(texts: list[str]) -> list[list[float]]:
    all_embeddings = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch_texts = texts[i:i + BATCH_SIZE]

        response = post_with_retry(
            RENDER_EMBEDDING_URL,
            json={"texts": batch_texts},
            timeout=TIMEOUT,
            retries=RETRIES,
            backoff_factor=BACKOFF_FACTOR
        )

        if response is None:
            print(f"Skipping batch {i // BATCH_SIZE + 1} due to repeated failures.")
            continue

        try:
            remote_batch_embeddings = np.array(response.json()["embeddings"])

            norms = np.linalg.norm(remote_batch_embeddings, axis=1, keepdims=True)
            remote_batch_embeddings = remote_batch_embeddings / np.clip(norms, a_min=1e-9, a_max=None)

            all_embeddings.extend(remote_batch_embeddings.tolist())

        except Exception as e:
            print(f"Error parsing or normalizing batch {i // BATCH_SIZE + 1}: {e}")
            continue

    return all_embeddings
