from fastapi import APIRouter, HTTPException
from models.schema import TranscriptRequest, TranscriptChunk
from services.transcript_utils import fetch_and_chunk_transcript
from vector_store.embedder import embed_texts
from vector_store.faiss_store import add_to_index
from vector_store.db_store import save_metadata , is_video_already_stored
from models.schema import ChunkEmbeddingRequest

router = APIRouter()

@router.post("/fetch", response_model=list[TranscriptChunk])
def fetch_transcript(data: TranscriptRequest):
    try:
        chunks, video_id = fetch_and_chunk_transcript(data.url)
        for chunk in chunks:
            chunk["video_id"] = video_id
        return chunks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/embed-store")
def embed_and_store(data: ChunkEmbeddingRequest):
    chunks = data.chunks
    texts = [chunk.text for chunk in chunks]

    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks provided.")

    video_id = chunks[0].video_id  

    if is_video_already_stored(video_id):
        return {"status": "duplicate", "message": f"Video {video_id} already stored."}

    embeddings = embed_texts(texts)
    ids = add_to_index(embeddings)
    save_metadata(ids, chunks, video_id)

    return {"status": "success", "stored": len(ids)}
