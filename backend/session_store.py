from cachetools import LRUCache
from threading import Lock
from vector_store.faiss_store import get_faiss_index
import time

session_store = LRUCache(maxsize=5)
session_lock = Lock()

SESSION_TTL_SECONDS = 600  

def clean_expired_sessions():
    with session_lock:
        now = time.time()
        expired_keys = [
            session_id for session_id, session_data in session_store.items()
            if now - session_data.get("created_at", 0) > SESSION_TTL_SECONDS
        ]
        for session_id in expired_keys:
            session_store.pop(session_id, None)

def init_session(session_id: str, embedding_dim: int):
    clean_expired_sessions()

    with session_lock:
        if session_id not in session_store:
            session_store[session_id] = {
                "faiss_index": get_faiss_index(embedding_dim),
                "metadata": {},
                "timestamps": {},
                "created_at": time.time(),
            }

def clear_session(session_id: str):
    with session_lock:
        session_store.pop(session_id, None)

def get_session_index(session_id: str):
    return session_store[session_id]["faiss_index"]

def get_session_metadata(session_id: str):
    return session_store[session_id]["metadata"]

def get_session_timestamps(session_id: str):
    return session_store[session_id]["timestamps"]
