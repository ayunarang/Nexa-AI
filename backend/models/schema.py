from pydantic import BaseModel

class TranscriptRequest(BaseModel):
    url: str

class TranscriptChunk(BaseModel):
    start: float
    end: float
    text: str
    video_id: str 

class ChunkEmbeddingRequest(BaseModel):
    chunks: list[TranscriptChunk]


class ClearSessionRequest(BaseModel):
    session_id: str