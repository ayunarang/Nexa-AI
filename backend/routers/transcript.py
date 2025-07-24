from fastapi import APIRouter, HTTPException
from models.schema import TranscriptRequest, TranscriptChunk, ClearSessionRequest
from utils.transcript_utils import fetch_and_chunk_transcript
from session_store import init_session, clear_session, get_session_index, get_session_metadata
from vector_store.embedder import embed_texts
from vector_store.faiss_store import add_to_index

from uuid import uuid4
import traceback

router = APIRouter()

@router.post("/fetch", response_model=TranscriptChunk)
def fetch_transcript_and_store(data: TranscriptRequest):
    try:
        # Step 0: Generate a new session ID
        session_id = str(uuid4())

        # Step 1: Fetch and chunk transcript
        chunks, video_id = fetch_and_chunk_transcript(data.url)
        for i, chunk in enumerate(chunks):
            chunk["id"] = i 
            chunk["video_id"] = video_id


        # Step 2: Generate embeddings 
        texts = [chunk['text'] for chunk in chunks]
        embeddings = embed_texts(texts)
        if not embeddings:
            raise ValueError("No embeddings generated.")
        
        # Step 3: Initialize session
        init_session(session_id)

        session_index = get_session_index(session_id)
        metadata = get_session_metadata(session_id)

        if video_id in metadata:
            return {
                "status": "Duplicate",
                "video_id": video_id,
                "session_id": session_id
            }

        # Step 4: Add to FAISS index and get integer IDs
        chunk_ids = [chunk["id"] for chunk in chunks]

        if len(texts) != len(embeddings):
            for i, (text, emb) in enumerate(zip(texts, embeddings)):
                print(f"[{i}] text length: {len(text)} | embedding: {type(emb)} shape: {getattr(emb, 'shape', 'no shape')}")


        ids = add_to_index(session_index, embeddings, chunk_ids)


        # Step 5: Store metadata with integer IDs consistently
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
            "session_id": session_id
        }

    except Exception as e:
        traceback.print_exc()
        if str(e) == "The video is not in English.":
            raise HTTPException(status_code=400, detail="The video is not in English.")
        elif str(e) == "Transcript not available.":
            raise HTTPException(status_code=400, detail="The video does not have subtitles.")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/clear-session")
def clear_user_session(data: ClearSessionRequest):
    try:
        clear_session(data.session_id)
        return {"status": "cleared", "session_id": data.session_id}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
