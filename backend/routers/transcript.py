from fastapi import APIRouter, HTTPException
from models.schema import TranscriptRequest, TranscriptChunk
from services.transcript_utils import fetch_and_chunk_transcript

router = APIRouter()

@router.post("/fetch", response_model=list[TranscriptChunk])
def fetch_transcript(data: TranscriptRequest):
    try:
        return fetch_and_chunk_transcript(data.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
