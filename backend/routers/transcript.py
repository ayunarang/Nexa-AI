from fastapi import APIRouter, HTTPException, Query
from models.schema import TranscriptRequest, TranscriptChunk, ChunkEmbeddingRequest, ClearSessionRequest
from services.transcript_utils import fetch_and_chunk_transcript
from vector_store.embedder import embed_texts
from vector_store.faiss_store import add_to_index
from uuid import uuid4
from session_store import init_session, clear_session, get_session_index, get_session_metadata

import traceback  

router = APIRouter()

@router.post("/fetch", response_model=list[TranscriptChunk])
def fetch_transcript(data: TranscriptRequest, session_id: str = Query(None)):
    try:
        chunks, video_id = fetch_and_chunk_transcript(data.url)
        for chunk in chunks:
            chunk['video_id'] = video_id
        return chunks

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embed-store")
def embed_and_store(data: ChunkEmbeddingRequest, session_id: str = Query(...)):
    from session_store import get_session_index, get_session_metadata

    try:

        chunks = data.chunks
        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks provided.")

        video_id = chunks[0].video_id
        metadata = get_session_metadata(session_id)

        if video_id in metadata:
            return {"status": "duplicate", "message": f"Video {video_id} already stored in session."}

        texts = [chunk.text for chunk in chunks]
        embeddings = embed_texts(texts)

        index = get_session_index(session_id)
        ids = add_to_index(index, embeddings)

        metadata[video_id] = [
            {
                "id": _id,
                "start": chunk.start,
                "end": chunk.end,
                "text": chunk.text
            }
            for _id, chunk in zip(ids, chunks)
        ]

        return {"status": "success", "stored": len(ids)}

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
def clear_user_session(data: ClearSessionRequest):
    try:
        session_id = data.session_id
        clear_session(session_id)
        return {"status": "cleared", "session_id": session_id}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))