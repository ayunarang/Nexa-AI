from cachetools import LRUCache
from threading import Lock
from vector_store.faiss_store import get_faiss_index

session_store = LRUCache(maxsize=100)
session_lock = Lock()

def init_session(session_id: str):
    with session_lock:
        if session_id not in session_store:
            session_store[session_id] = {
                "faiss_index": get_faiss_index(),
                "metadata": {},
                "timestamps": {},
            }

def clear_session(session_id: str):
    with session_lock:
        session_store.pop(session_id, None)

def get_session_index(session_id: str):
    init_session(session_id)
    return session_store[session_id]["faiss_index"]

def get_session_metadata(session_id: str):
    init_session(session_id)
    return session_store[session_id]["metadata"]

def get_session_timestamps(session_id: str):
    init_session(session_id)
    return session_store[session_id]["timestamps"]
