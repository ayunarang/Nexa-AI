from fastapi import APIRouter, HTTPException
from models.schema import TranscriptRequest, TranscriptChunk, ClearSessionRequest
from utils.transcript_utils import fetch_and_chunk_transcript
from session_store import init_session, clear_session, get_session_index, get_session_metadata
from uuid import uuid4
import traceback

router = APIRouter()

@router.post("/fetch", response_model=TranscriptChunk)
def fetch_transcript_and_store(data: TranscriptRequest):
    try:
        # Step 0: Generate a new session ID 
        session_id = str(uuid4())

        # Step 1: Fetch and chunk the transcript
        chunks, video_id = fetch_and_chunk_transcript(data.url)
        for chunk in chunks:
            chunk['video_id'] = video_id

        # Step 2: Generate embeddings
        from vector_store.embedder import embed_texts
        texts = [chunk['text'] for chunk in chunks]
        embeddings = embed_texts(texts)

        init_session(session_id)

        metadata = get_session_metadata(session_id)
        if video_id in metadata:
            return {"status": "Duplicate", "video_id": video_id, "session_id": session_id}

        # Step 3: Add embeddings to FAISS index
        from vector_store.faiss_store import add_to_index
        index = get_session_index(session_id)
        ids = add_to_index(index, embeddings)

        # Step 4: Store metadata
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
            "session_id": session_id,  
        }

    except Exception as e:
        traceback.print_exc()
        if str(e) == "The video is not in English.":
            raise HTTPException(status_code=400, detail="The video is not in English.")
        elif str(e) == "Transcript not available.":
            raise HTTPException(status_code=400, detail="The video does not have subtitles.")
        raise HTTPException(status_code=500, detail="Internal server error.")



@router.post("/clear-session")
def clear_user_session(data: ClearSessionRequest):
    try:
        clear_session(data.session_id)
        return {"status": "cleared", "session_id": data.session_id}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
