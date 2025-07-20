from fastapi import APIRouter, HTTPException, Query
from models.schema import TranscriptRequest, TranscriptChunk
from utils.transcript_utils import fetch_and_chunk_transcript
from session_store import init_session, clear_session, get_session_index, get_session_metadata
from uuid import uuid4
import traceback

router = APIRouter()

@router.post("/fetch", response_model=TranscriptChunk)
def fetch_transcript_and_store(data: TranscriptRequest, session_id: str = Query(...)):
    try:
        chunks, video_id = fetch_and_chunk_transcript(data.url)
        for chunk in chunks:
            chunk['video_id'] = video_id

        metadata = get_session_metadata(session_id)
        if video_id in metadata:
            return {"status": "Duplicate", "video_id": video_id }

        from vector_store.embedder import embed_texts
        texts = [chunk['text'] for chunk in chunks]
        embeddings = embed_texts(texts)

        from vector_store.faiss_store import add_to_index
        index = get_session_index(session_id)
        ids = add_to_index(index, embeddings)

        metadata[video_id] = [
            {
                "id": _id,
                "start": chunk['start'],
                "end": chunk['end'],
                "text": chunk['text']
            }
            for _id, chunk in zip(ids, chunks)
        ]

        return {
            "status": "Success",
            "video_id": video_id,
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/init-session")
def init_new_session():
    try:
        session_id = str(uuid4())
        init_session(session_id)
        return {"session_id": session_id}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear-session")
def clear_user_session(data: dict):
    try:
        session_id = data.get("session_id")
        clear_session(session_id)
        return {"status": "cleared", "session_id": session_id}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
